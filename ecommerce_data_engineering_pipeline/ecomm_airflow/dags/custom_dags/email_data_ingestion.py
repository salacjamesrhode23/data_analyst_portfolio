import os
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable

from custom_functions.ingest_data_email.fetch_email import fetch_email
from custom_functions.ingest_data_email.parse_email import email_orders_to_gcs

# --- DAG Definition ---
with DAG(
    dag_id="ingest_email_orders",
    start_date=datetime(2025, 11, 22),
    schedule="@daily",
    catchup=False
) as dag:

    # ---------------------------
    # Task 1: Fetch Email Bodies
    # ---------------------------
    def fetch_email_task(**kwargs):
        subject_filter = '"[demo-store] Order Confirmation for"'
        user = Variable.get("EMAIL_USER")
        password = Variable.get("EMAIL_PASSWORD")

        # Fetch email bodies
        email_bodies = fetch_email(user=user, password=password, subject_filter=subject_filter)

        # Push to XCom for downstream tasks
        kwargs['ti'].xcom_push(key='email_bodies', value=email_bodies)

    fetch_emails = PythonOperator(
        task_id='fetch_email_bodies',
        python_callable=fetch_email_task
    )

    # ---------------------------
    # Task 2: Process Emails and Upload to GCS
    # ---------------------------
    def email_orders_to_gcs_task(**kwargs):
        ti = kwargs['ti']
        email_bodies = ti.xcom_pull(key='email_bodies', task_ids='fetch_email_bodies')

        if email_bodies:
            email_orders_to_gcs(email_bodies)
        else:
            print("No email bodies found.")

    upload_to_gcs = PythonOperator(
        task_id='email_orders_to_gcs',
        python_callable=email_orders_to_gcs_task
    )

    # ---------------------------
    # Set task dependencies
    # ---------------------------
    fetch_emails >> upload_to_gcs
