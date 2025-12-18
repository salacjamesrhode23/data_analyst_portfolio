import random
from datetime import datetime, timedelta
from typing import List

import pandas as pd
from faker import Faker
from sqlalchemy import create_engine
from google.cloud.sql.connector import Connector

# -----------------------------
# Constants / Globals
# -----------------------------
faker = Faker("en_PH")
connector = Connector()

# -----------------------------
# Utility Functions
# -----------------------------
def generate_reference(prefix: str = "#") -> str:
    return f"{prefix}{random.randint(100_000_000_000, 999_999_999_999)}"


def normalize_columns(record: dict) -> dict:
    """Lowercase and snake_case column names."""
    return {k.lower().replace(" ", "_"): v for k, v in record.items()}


def compute_row_count(
    start_date: datetime,
    end_date: datetime,
    avg_daily_txn: int
) -> int:
    return (end_date - start_date).days * avg_daily_txn

# -----------------------------
# Data Loading / Preparation
# -----------------------------
def load_customers(customer_csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(customer_csv_path)
    return df.drop(columns=["First Name", "Last Name"])


def load_products(product_csv_path: str) -> pd.DataFrame:
    return pd.read_csv(product_csv_path)


def dataframe_to_lookup(
    df: pd.DataFrame,
    key_col: str
) -> dict:
    return (
        df.drop_duplicates(subset=[key_col])
          .set_index(key_col)
          .to_dict("index")
    )

# -----------------------------
# Order Generation
# -----------------------------
def generate_single_order(
    customers: List[str],
    products: List[str],
    customer_lookup: dict,
    product_lookup: dict,
    payment_methods: List[str],
    start_date: datetime,
    end_date: datetime
) -> List[dict]:

    order_number = generate_reference()
    order_date = faker.date_time_between_dates(
        datetime_start=start_date,
        datetime_end=end_date
    )

    billing_name = random.choice(customers)
    payment_method = random.choice(payment_methods)
    payment_reference = generate_reference()

    records = []

    for _ in range(random.randint(1, 3)):
        product_name = random.choice(products)

        record = {
            "order_number": order_number,
            "order_date": order_date,
            "billing_name": billing_name,
            "lineitem_name": product_name,
            "lineitem_qty": random.randint(1, 3),
            "payment_method": payment_method,
            "payment_reference": payment_reference,
            "payment_date": order_date + timedelta(days=random.uniform(0, 1)),
            "fulfillment_date": order_date + timedelta(days=random.uniform(1, 2)),
        }

        record.update(normalize_columns(customer_lookup[billing_name]))
        record.update(normalize_columns(product_lookup[product_name]))

        records.append(record)

    return records

def generate_orders(
    customers_df: pd.DataFrame,
    products_df: pd.DataFrame,
    payment_methods: List[str],
    start_date: datetime,
    end_date: datetime,
    avg_daily_txn: int
) -> pd.DataFrame:

    customers = customers_df["Full Name"].tolist()
    products = products_df["Title"].tolist()

    customer_lookup = dataframe_to_lookup(customers_df, "Full Name")
    product_lookup = dataframe_to_lookup(products_df, "Title")

    total_rows = compute_row_count(start_date, end_date, avg_daily_txn)

    data = []
    for _ in range(total_rows):
        data.extend(
            generate_single_order(
                customers,
                products,
                customer_lookup,
                product_lookup,
                payment_methods,
                start_date,
                end_date,
            )
        )

    return pd.DataFrame(data)

# -----------------------------
# Database
# -----------------------------
def create_cloudsql_engine(
    instance_connection_name: str,
    db_user: str,
    db_pass: str,
    db_name: str
):

    def getconn():
        return connector.connect(
            instance_connection_name,
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name,
        )

    return create_engine("postgresql+pg8000://", creator=getconn)

def save_dataframe(
    df: pd.DataFrame,
    engine,
    table_name: str
) -> dict:
    row_count = len(df)

    if row_count == 0:
        return {
            "success": True,
            "rows_inserted": 0,
            "table": table_name,
            "message": "No rows to insert",
        }

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="append",
        index=False,
    )

    return {
        "success": True,
        "rows_inserted": row_count,
        "table": table_name,
        "message": "Data successfully inserted",
    }

# -----------------------------
# Orchestrator (Main Entry Point)
# -----------------------------
def generate_and_save_orders(
    customer_csv_path: str,
    product_csv_path: str,
    payment_methods: List[str] = None,
    start_date: datetime = datetime(2025, 12, 12),
    end_date: datetime = datetime(2025, 12, 13),
    average_daily_transaction: int = 100,
    instance_connection_name: str = "project-id:region:instance-name",
    db_user: str = "db_user",
    db_pass: str = "db_password",
    db_name: str = "my_database",
    table_name: str = "orders",
) -> dict:


    if payment_methods is None:
        payment_methods = [
            "PayPal",
            "Digital Wallet",
            "Cash on Delivery",
            "Bank Transfer",
        ]
    
    customers_df = load_customers(customer_csv_path)
    products_df = load_products(product_csv_path)

    orders_df = generate_orders(
        customers_df,
        products_df,
        payment_methods,
        start_date,
        end_date,
        average_daily_transaction,
    )

    engine = create_cloudsql_engine(
        instance_connection_name,
        db_user,
        db_pass,
        db_name,
    )

    result = save_dataframe(orders_df, engine, table_name)

    return result