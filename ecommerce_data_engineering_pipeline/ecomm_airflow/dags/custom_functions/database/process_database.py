from airflow.models import Variable
import pendulum

from custom_functions import read_state, write_state, upload_df_to_gcs
from .fetch_database import fetch_database_orders


# ---------------------------
# GCS STATE MANAGEMENT
# ---------------------------
# def read_state(bucket_name: str, state_file: str) -> dict:
#     client = storage.Client()
#     bucket = client.bucket(bucket_name)
#     blob = bucket.blob(state_file)

#     if not blob.exists():
#         return {"last_row_id": 0}

#     content = blob.download_as_text()
#     return json.loads(content)

# def write_state(bucket_name: str, state_file: str, state_dict: dict):
#     client = storage.Client()
#     bucket = client.bucket(bucket_name)
#     blob = bucket.blob(state_file)
#     blob.upload_from_string(json.dumps(state_dict), content_type="application/json")

# ---------------------------
# CLOUD SQL CONNECTION
# ---------------------------
# connector = Connector()  # reuse connector across calls

# def get_postgres_engine(instance_connection_name: str, db_user: str, db_pass: str, db_name: str):

#     def getconn():
#         return connector.connect(
#             instance_connection_name,
#             "pg8000",
#             user=db_user,
#             password=db_pass,
#             db=db_name
#         )

#     engine = create_engine("postgresql+pg8000://", creator=getconn)
#     return engine

# def fetch_database_orders(
#     instance_connection_name: str,
#     db_user: str,
#     db_pass: str,
#     db_name: str,
#     last_row_id: int
# ) -> pd.DataFrame:
#     engine = get_postgres_engine(instance_connection_name, db_user, db_pass, db_name)

#     query = f"""
#         SELECT *
#         FROM orders
#         WHERE row_id > {last_row_id}
#         ORDER BY row_id ASC;
#     """

#     df = pd.read_sql(query, engine)
#     return df

# ---------------------------
# UPLOAD TO GCS
# ---------------------------
# def upload_df_to_gcs(df: pd.DataFrame, bucket_name: str, file_name: str) -> None:
#     """
#     Convert DataFrame to CSV and upload to GCS.
#     """
#     csv_buffer = StringIO()
#     df.to_csv(csv_buffer, index=False, quoting=csv.QUOTE_ALL, encoding="utf-8-sig")
#     csv_data = csv_buffer.getvalue()

#     client = storage.Client()
#     bucket = client.bucket(bucket_name)
#     blob = bucket.blob(file_name)
#     blob.upload_from_string(csv_data, content_type="text/csv")


# ---------------------------
# MAIN ORCHESTRATION
# ---------------------------
def process_database_orders(bucket_name: str):
    """
    Main ETL: 
    - Read state
    - Fetch new rows using row_id > last_row_id
    - Upload to GCS
    - Update state with max row_id
    """
    # Cloud SQL credentials from environment or variables
    instance_connection_name = "de-project-ecomm:asia-southeast1:ecomm-db"
    db_user = "airflow"
    db_pass = Variable.get("DB_PASSWORD")
    db_name = "ecomm_db"

    state_file = "idempotency_keys/db_orders_state.json"

    # Step 1: Load last row_id processed
    state = read_state(bucket_name, state_file)
    last_row_id = int(state["last_row_id"])

    # Step 2: Fetch new rows
    df = fetch_database_orders(instance_connection_name, db_user, db_pass, db_name, last_row_id)

    if df.empty:
        print("No new transactions to process.")
        return None

    # Step 3: Upload result CSV to GCS
    now = pendulum.now()
    file_name = f"from_database/orders_{now.to_datetime_string().replace(':','').replace(' ','_')}.csv"
    upload_df_to_gcs(df, bucket_name, file_name)

    # Step 4: Update the state with the newest row_id
    new_last_row_id = int(df["row_id"].max())
    write_state(bucket_name, state_file, {"last_row_id": new_last_row_id}, {"last_row_id": 0})

    print(f"Processed {len(df)} rows and uploaded to {file_name}")
    return file_name