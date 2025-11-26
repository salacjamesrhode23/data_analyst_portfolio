# dags/ingest_multi_datasets_taskflow.py
from datetime import datetime
from docker.types import Mount
import tempfile
import os
import requests

from airflow import DAG
from airflow.decorators import task
from airflow.models import Variable
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

# --- CONFIG: add more datasets here ---
DATASETS = [
    {
        "name": "accounts",
        "url_variable": "accounts_csv_url",
        "table": "accounts",
        "create_sql": "sql/create_table_accounts.sql"
    },
    {
        "name": "products",
        "url_variable": "products_csv_url",
        "table": "products",
        "create_sql": "sql/create_table_products.sql"
    },
    {
        "name": "sales_teams",
        "url_variable": "sales_teams_csv_url",
        "table": "sales_teams",
        "create_sql": "sql/create_table_sales_pipeline.sql"
    },
    {
        "name": "sales_pipeline",
        "url_variable": "sales_pipeline_csv_url",
        "table": "sales_pipeline",
        "create_sql": "sql/create_table_sales_teams.sql"
    },
]

DEFAULT_ARGS = {"retries": 1}

DBT_PROJECT_PATH = "C:/Users/Administrator/data_analyst_portfolio/maven_sales_challenge/postgres/dbt_project" 

with DAG(
    dag_id="ingest_multiple_csvs_taskflow",
    start_date=datetime(2025, 11, 22),
    schedule="@daily",
    catchup=False,
    default_args=DEFAULT_ARGS,
    max_active_runs=1,
    tags=["ingest"]
) as dag:

    # --- Step 1: Create tables ---
    create_table_ops = {}
    for ds in DATASETS:
        create_table_ops[ds["name"]] = SQLExecuteQueryOperator(
            task_id=f"create_table__{ds['name']}",
            sql=ds["create_sql"],
            conn_id="postgres_conn",
        )

    # --- Step 2: Ingest all datasets in one TaskFlow task ---
    @task
    def ingest_all_datasets(dataset_configs):
        """Download and copy each dataset CSV into Postgres."""
        for cfg in dataset_configs:
            # 1️⃣ Get CSV URL from Airflow Variable
            url = Variable.get(cfg["url_variable"])
            # 2️⃣ Download CSV to temp file
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
            tmp_file.write(response.content)
            tmp_file.flush()
            tmp_file.close()
            # 3️⃣ Copy into Postgres
            hook = PostgresHook(postgres_conn_id="postgres_conn")
            sql = f"COPY {cfg['table']} FROM STDIN WITH CSV HEADER DELIMITER ','"
            hook.copy_expert(sql=sql, filename=tmp_file.name)  # pass path as string
            # 4️⃣ Cleanup
            try:
                os.remove(tmp_file.name)
            except Exception:
                pass

    # --- Step 3: Set dependencies ---
    ingest_task = ingest_all_datasets(DATASETS)

    for ds in DATASETS:
        create_table_ops[ds["name"]] >> ingest_task

    # --- Step 4: Dbt debug tasks in DockerOperator ---
    dbt_debug = DockerOperator(
        task_id="dbt_debug",
        image="maven_dbt:latest",  # replace with your dbt container image
        api_version='auto',
        auto_remove='force',
        command="debug --profiles-dir /usr/app/dbt",
        network_mode="maven-network",  # ensure it can reach Postgres
        # mounts=[{"source": DBT_PROJECT_PATH, "target": "/usr/app/dbt", "type": "bind"}],
        mounts=[Mount(source=DBT_PROJECT_PATH, target="/usr/app/dbt", type="bind")],

    )

    # --- Step 5: dbt deps ---
    dbt_deps = DockerOperator(
        task_id="dbt_deps",
        image="maven_dbt:latest",
        api_version="auto",
        auto_remove="force",
        command="deps --profiles-dir /usr/app/dbt",
        network_mode="maven-network",
        mounts=[Mount(source=DBT_PROJECT_PATH, target="/usr/app/dbt", type="bind")],
    )
    
    # --- Step 6: dbt run ---
    dbt_run = DockerOperator(
        task_id="dbt_run",
        image="maven_dbt:latest",
        api_version="auto",
        auto_remove="force",
        command="run --profiles-dir /usr/app/dbt",
        network_mode="maven-network",
        mounts=[Mount(source=DBT_PROJECT_PATH, target="/usr/app/dbt", type="bind")],
    )

    # --- Step 7: Chain dependencies ---
    ingest_task >> dbt_debug >> dbt_deps >> dbt_run
