from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
import pendulum

from custom_functions import (
    process_api_customers,
    process_api_products,
    load_csv_to_snowflake
)

with DAG(
    dag_id="ingest_api_dimension",
    start_date=pendulum.datetime(2025, 11, 22, tz=pendulum.timezone("Asia/Manila")),
    schedule=None,
    catchup=False,
) as dag:

    # ---------------------------
    # Task 1: Process api for customers and upload CSV to GCS
    # ---------------------------
    process_customers = PythonOperator(
        task_id="process_api_customers_to_gcs",
        python_callable=process_api_customers,
        op_kwargs={
            "base_url": Variable.get("BASE_URL"),
            "bucket_name": Variable.get("GCS_BUCKET"),
            "gcp_conn_id": "gcp_connection"
        }
    )

    # ---------------------------
    # Task 2: Process api for products and upload CSV to GCS
    # ---------------------------
    process_products = PythonOperator(
        task_id="process_api_products_to_gcs",
        python_callable=process_api_products,
        op_kwargs={
            "base_url": Variable.get("BASE_URL"),
            "page_limit": 50,
            "bucket_name": Variable.get("GCS_BUCKET"),
            "gcp_conn_id": "gcp_connection"
        }
    )

    # ---------------------------
    # Task 3A: Load Customers CSV into Snowflake
    # ---------------------------
    load_customers = PythonOperator(
        task_id="load_customers_to_snowflake",
        python_callable=load_csv_to_snowflake,
        op_kwargs={
            "table_name": "ECOMM.CUSTOMERS",
            "stage_name": "MY_GCS_STAGE",
            "file_name": "{{ ti.xcom_pull(task_ids='process_api_customers_to_gcs') }}"
        }
    )

    # ---------------------------
    # Task 3B: Load Products CSV into Snowflake
    # ---------------------------
    load_products = PythonOperator(
        task_id="load_products_to_snowflake",
        python_callable=load_csv_to_snowflake,
        op_kwargs={
            "table_name": "ECOMM.PRODUCTS",
            "stage_name": "MY_GCS_STAGE",
            "file_name": "{{ ti.xcom_pull(task_ids='process_api_products_to_gcs') }}"
        }
    )

    # Define task order
    process_customers >> load_customers
    process_products >> load_products