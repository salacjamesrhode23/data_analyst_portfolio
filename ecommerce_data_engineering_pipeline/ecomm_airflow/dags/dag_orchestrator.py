from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
import pendulum

with DAG(
    dag_id="orchestrator_elt_pipeline",
    start_date=pendulum.datetime(2025, 11, 22, tz=pendulum.timezone("Asia/Manila")),
    schedule="30 10 * * *",
    catchup=False
) as dag:
    
    # ---------------------------
    # Task 1: Trigger the API dimension ingestion DAG
    # ---------------------------
    trigger_ingest_api_dimension = TriggerDagRunOperator(
        task_id="trigger_api_ingestion",
        trigger_dag_id="ingest_api_dimension",
        wait_for_completion=True,
        poke_interval=30,
        conf={"triggered_by": "orchestrator_elt_pipeline"},
    )

    # ---------------------------
    # Task 2: Trigger the Database orders ingestion DAG
    # ---------------------------
    trigger_ingest_database_orders = TriggerDagRunOperator(
        task_id="trigger_database_ingestion",
        trigger_dag_id="ingest_database_orders",  # Second DAG
        wait_for_completion=True,
        poke_interval=30,
        conf={"triggered_by": "orchestrator_elt_pipeline"},
    )

    # ---------------------------
    # Task 3: Trigger the Email orders ingestion DAG
    # ---------------------------
    trigger_ingest_email_orders = TriggerDagRunOperator(
        task_id="trigger_email_ingestion",
        trigger_dag_id="ingest_email_orders",
        wait_for_completion=True,
        poke_interval=30,
        conf={"triggered_by": "orchestrator_elt_pipeline"},
    )

    # ---------------------------
    # Task 4: Trigger the dbt operations DAG
    # ---------------------------
    trigger_execute_dbt = TriggerDagRunOperator(
        task_id="trigger_dbt_operations",
        trigger_dag_id="execute_dbt_operations",
        wait_for_completion=True,
        poke_interval=30,
        conf={"triggered_by": "orchestrator_elt_pipeline"},
    )

    # Define execution order:
    trigger_ingest_api_dimension >> [trigger_ingest_database_orders, trigger_ingest_email_orders] >> trigger_execute_dbt