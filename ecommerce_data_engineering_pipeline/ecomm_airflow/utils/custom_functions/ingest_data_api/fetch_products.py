import requests
import pandas as pd
import csv

def fetch_products_to_csv(base_url, product_csv_path, page_limit):
    products_data = []
    page = 1

    while True:
        response = requests.get(f"{base_url}/products?page={page}&limit={page_limit}")
        if response.status_code != 200:
            print(f"Error fetching products: {response.status_code}")
            break
        
        data = response.json()
        if not data:
            break

        products_data.extend(data)
        page += 1

    if products_data:
        df_products = pd.DataFrame(products_data)
        df_products.to_csv(product_csv_path, index=False, encoding="utf-8-sig", quoting=csv.QUOTE_ALL)
        print(f"Saved to {product_csv_path}")
        return df_products
    else:
        print("No products data retrieved")
        return None