# Standard library
import csv
import requests
import pandas as pd

# Third-party libraries
from io import StringIO
# from google.cloud import storage
from airflow.providers.google.cloud.hooks.gcs import GCSHook


# -----------------------------
# FETCH API FUNCTION
# -----------------------------
def fetch_customers_from_api(base_url):

    """
    Fetch customers from API endpoint /customers and return as DataFrame.
    """
    
    response = requests.get(f"{base_url}/customers")
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        return df
    else:
        print(f"Error fetching customers: {response.status_code}")
        return None

# ---------------------------
# UPLOAD TO GCS FUNCTION
# ---------------------------
def upload_df_to_gcs(df: pd.DataFrame, bucket_name: str, file_name: str, gcp_conn_id="gcp_connection") -> None:

    """
    Convert Dataframe to csv then upload to GCS bucket
    """

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False, quoting=csv.QUOTE_ALL, encoding="utf-8-sig")
    csv_data = csv_buffer.getvalue()

    hook = GCSHook(gcp_conn_id=gcp_conn_id)
    hook.upload(bucket_name=bucket_name, object_name=file_name, data=csv_data)

    # client = storage.Client()
    # bucket = client.bucket(bucket_name)
    # blob = bucket.blob(file_name)
    # blob.upload_from_string(csv_data, content_type="text/csv")
    

# ---------------------------
# ORCHESTRATION FUNCTION
# ---------------------------
def process_api_customers(
    base_url: str,
    bucket_name: str,
    gcp_conn_id="gcp_connection"
) -> str:

    """
    Main orchestration function: fetch customers → upload CSV.
    Returns file name uploaded to GCS.
    """
    # Step 1: Fetch customer
    df = fetch_customers_from_api(base_url)

    # Step 2: Upload DataFrame to CSV in GCS
    file_name = "from_api/customers_latest.csv"
    upload_df_to_gcs(df, bucket_name, file_name, gcp_conn_id=gcp_conn_id)

    return file_name