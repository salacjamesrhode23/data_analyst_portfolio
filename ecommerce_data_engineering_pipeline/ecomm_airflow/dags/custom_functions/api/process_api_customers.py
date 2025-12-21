import requests
import pandas as pd

from custom_functions import upload_df_to_gcs

def fetch_customers_from_api(base_url):
    response = requests.get(f"{base_url}/customers")
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        return df
    else:
        print(f"Error fetching customers: {response.status_code}")
        return None


# def upload_df_to_gcs(df: pd.DataFrame, bucket_name: str, file_name: str) -> None:

#     """
#     Convert Dataframe to csv then upload to GCS bucket
#     """

#     csv_buffer = StringIO()
#     df.to_csv(csv_buffer, index=False, quoting=csv.QUOTE_ALL, encoding="utf-8-sig")
#     csv_data = csv_buffer.getvalue()

#     client = storage.Client()
#     bucket = client.bucket(bucket_name)
#     blob = bucket.blob(file_name)
#     blob.upload_from_string(csv_data, content_type="text/csv")
    
def process_api_customers(
    base_url: str,
    bucket_name: str
) -> str:

    df = fetch_customers_from_api(base_url)

    file_name = "from_api/customers_latest.csv"
    upload_df_to_gcs(df, bucket_name, file_name)

    return file_name