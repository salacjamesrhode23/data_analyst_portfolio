import csv
import pandas as pd
from io import StringIO
from airflow.providers.postgres.hooks.postgres import PostgresHook
from google.cloud import storage
import pendulum
import json

# ---------------------------
# GCS STATE MANAGEMENT
# ---------------------------
def read_state(bucket_name: str, state_file: str) -> dict:
    """
    Reads last processed row_id from GCS.
    If the state file does not exist, return last_row_id = 0.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(state_file)

    if not blob.exists():
        # First run
        return {"last_row_id": 0}

    content = blob.download_as_text()
    return json.loads(content)


def write_state(bucket_name: str, state_file: str, state_dict: dict):
    """
    Writes last processed row_id into GCS.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(state_file)

    blob.upload_from_string(
        json.dumps(state_dict),
        content_type="application/json"
    )

# ---------------------------
# FETCH FROM POSTGRES (ROW-ID)
# ---------------------------
def fetch_database_orders(postgres_conn_id: str, last_row_id: int) -> pd.DataFrame:
    """
    Fetches only new rows from orders table using row_id-based incremental load.
    """
    pg_hook = PostgresHook(postgres_conn_id=postgres_conn_id)
    engine = pg_hook.get_sqlalchemy_engine()

    query = f"""
        SELECT *
        FROM orders
        WHERE row_id > {last_row_id}
        ORDER BY row_id ASC;
    """

    df = pd.read_sql(query, engine)
    return df

# ---------------------------
# UPLOAD TO GCS
# ---------------------------
def upload_df_to_gcs(df: pd.DataFrame, bucket_name: str, file_name: str) -> None:
    """
    Convert DataFrame to CSV and upload to GCS.
    """
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False, quoting=csv.QUOTE_ALL, encoding="utf-8-sig")
    csv_data = csv_buffer.getvalue()

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_string(csv_data, content_type="text/csv")


# ---------------------------
# MAIN ORCHESTRATION
# ---------------------------
def process_database_orders(
    postgres_conn_id: str,
    bucket_name: str
):
    """
    Main ETL: 
    - Read state
    - Fetch new rows using row_id > last_row_id
    - Upload to GCS
    - Update state with max row_id
    """
    state_file = "etl_state/db_orders_state.json"

    # Step 1: Load last row_id processed
    state = read_state(bucket_name, state_file)
    last_row_id = int(state["last_row_id"])

    # Step 2: Fetch new rows
    df = fetch_database_orders(postgres_conn_id, last_row_id)

    if df.empty:
        print("No new transactions to process.")
        return None

    # Step 3: Upload result CSV to GCS
    now = pendulum.now()
    file_name = (
        f"from_database/orders_{now.to_datetime_string().replace(':','').replace(' ','_')}.csv"
    )
    upload_df_to_gcs(df, bucket_name, file_name)

    # Step 4: Update the state with the newest row_id
    new_last_row_id = int(df["row_id"].max())
    write_state(bucket_name, state_file, {"last_row_id": new_last_row_id})

    print(f"Processed {len(df)} rows and uploaded to {file_name}")
    return file_name
