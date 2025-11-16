import warnings
warnings.filterwarnings("ignore")

import os
import csv
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from google.cloud import storage

# --- PostgreSQL connection ---
db_user = "postgres"
db_pass = "dR4m%T6nb"
db_host = "10.98.224.5"
db_port = "5432"
db_name = "db_ecomm"

engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}")

# --- Query your data ---
query = "SELECT * FROM orders;"
orders_df = pd.read_sql(query, engine)

# Delete after
mid = len(orders_df) // 2

df1 = orders_df.iloc[:mid]
df2 = orders_df.iloc[mid:]

orders_df = df2


# Initialize GCS client and bucket
client = storage.Client()
bucket = client.get_bucket('ecomm_bucket001')

# Generate a unique filename with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file_name = f'output_files/from_database/orders_{timestamp}.csv'

bucket.blob(file_name).upload_from_string(
    orders_df.to_csv(
        index=False,
        quoting=csv.QUOTE_ALL,
        encoding="utf-8-sig"
    ),
    content_type='text/csv'
)

