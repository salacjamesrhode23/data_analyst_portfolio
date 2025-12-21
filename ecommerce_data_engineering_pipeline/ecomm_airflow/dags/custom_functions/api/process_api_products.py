import requests
import pandas as pd

from custom_functions import upload_df_to_gcs

def fetch_products_from_api(base_url: str, page_limit: int) -> pd.DataFrame:

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
    


def process_api_products(base_url: str, page_limit: int, bucket_name: str) -> str:

    df = fetch_products_from_api(base_url, page_limit)

    file_name = "from_api/products_latest.csv"
    upload_df_to_gcs(df, bucket_name, file_name)

    return file_name