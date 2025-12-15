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
def fetch_products_from_api(base_url: str, page_limit: int) -> pd.DataFrame:

    """
    Fetch products from API paginated endpoint and return as DataFrame.
    """

    products_data = []
    page = 1

    while True:
        try:
            response = requests.get(f"{base_url}/products?page={page}&limit={page_limit}", timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to fetch products: {e}")

        data = response.json()
        if not data:
            break

        products_data.extend(data)
        page += 1

    if not products_data:
        raise ValueError("No products returned from API.")

    df = pd.DataFrame(products_data)
    return df

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
def process_api_products(
    base_url: str,
    page_limit: int,
    bucket_name: str,
    gcp_conn_id="gcp_connection"
) -> str:

    """
    Main orchestration function: fetch products → upload CSV.
    Returns file name uploaded to GCS.
    """
    # Step 1: Fetch products
    df = fetch_products_from_api(base_url, page_limit)

    # Step 2: Upload DataFrame to CSV in GCS
    file_name = "from_api/products_latest.csv"
    upload_df_to_gcs(df, bucket_name, file_name, gcp_conn_id=gcp_conn_id)

    return file_name