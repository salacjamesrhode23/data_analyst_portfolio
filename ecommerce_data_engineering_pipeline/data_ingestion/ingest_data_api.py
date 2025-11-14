import requests
import pandas as pd
from google.cloud import storage

# Initialize GCS client and bucket
client = storage.Client()
bucket = client.get_bucket('ecomm_bucket001')

base_url = "http://127.0.0.1:5000/api"

# --- Fetch all customers ---
response_customer = requests.get(f"{base_url}/customers")

if response_customer.status_code == 200:
    data = response_customer.json()
    df_customers = pd.DataFrame(data)
    bucket.blob('output_files/from_api/customers.csv').upload_from_string(
        df_customers.to_csv(index=False),
        content_type='text/csv'
    )
else:
    print(f"Error fetching customers: {response_customer.status_code}")

# --- Fetch all products (paginated) ---
products_data = []
page = 1
while True:
    response_product = requests.get(f"{base_url}/products", params={"page": page, "limit": 50})
    if response_product.status_code != 200:
        print(f"Error fetching products: {response_product.status_code}")
        break

    data = response_product.json()
    if not data:
        break

    products_data.extend(data)
    page += 1

if products_data:
    df_products = pd.DataFrame(products_data)
    bucket.blob('output_files/from_api/products.csv').upload_from_string(
        df_products.to_csv(index=False),
        content_type='text/csv'
    )
else:
    print("No product data retrieved.")
