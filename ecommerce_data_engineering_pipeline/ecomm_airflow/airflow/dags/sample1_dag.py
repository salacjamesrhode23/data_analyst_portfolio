from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "start_date": datetime(2024, 1, 1),
}

with DAG(
    dag_id="run_script_in_directory",
    default_args=default_args,
    schedule=None,
    catchup=False
) as dag:

    run_script = BashOperator(
        task_id="run_my_script",
        bash_command="""
        cd /home/salacjamesrhode23/data_analyst_portfolio/ecommerce_data_engineering_pipeline/faker_generator && \
        create_fake_customers.py
        """
    )
