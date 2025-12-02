import requests
import pandas as pd
import csv

def fetch_customers_to_csv(base_url, customer_csv_path):
    response = requests.get(f"{base_url}/customers")
    if response.status_code == 200:
        data = response.json()
        df_customers = pd.DataFrame(data)
        df_customers.to_csv(customer_csv_path, index=False, encoding="utf-8-sig", quoting=csv.QUOTE_ALL)
        print(f"Saved to {customer_csv_path}")
        return df_customers
    else:
        print(f"Error fetching customers: {response.status_code}")
        return None

