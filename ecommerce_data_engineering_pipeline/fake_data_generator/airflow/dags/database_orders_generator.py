from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
import pendulum

# from custom_functions.cloudsql.create_database_orders import generate_and_save_orders
from custom_functions import generate_and_save_orders

# --- DAG Definition ---
local_tz = pendulum.timezone("Asia/Manila")

with DAG(
    dag_id="generate_fake_cloudsql_orders",
    start_date=pendulum.datetime(2025, 12, 2, tz=local_tz),
    schedule="0 10 * * *",
    catchup=False,
    tags=["database", "postgres"]
) as dag:

    # Task 1: Generate Orders
    generate_orders_task = PythonOperator(
        task_id="generate_orders",
        python_callable=generate_and_save_orders,
        op_kwargs={
            "customer_csv_path": "/opt/airflow/data/fake_dbcustomers.csv",
            "product_csv_path": "/opt/airflow/data/fake_products.csv",
            # Cloud SQL connection info (ADC will handle auth)
            "instance_connection_name": "de-project-ecomm:asia-southeast1:ecomm-db",
            "db_user": "airflow",
            "db_pass": Variable.get("DB_PASSWORD"),
            "db_name": "ecomm_db",
            "table_name": "orders",
        },
    )
