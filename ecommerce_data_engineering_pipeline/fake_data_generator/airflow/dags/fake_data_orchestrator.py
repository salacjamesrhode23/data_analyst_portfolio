from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
import pendulum

with DAG(
    dag_id="fake_data_orchestrator",
    start_date=pendulum.datetime(2025, 12, 16, tz=pendulum.timezone("Asia/Manila")),
    schedule="6 22 * * *",
    catchup=False
) as dag:
    
    # ---------------------------
    # Task 1: Trigger email orders generator DAG
    # ---------------------------
    trigger_email_orders_generator = TriggerDagRunOperator(
        task_id="trigger_email_orders_generator",
        trigger_dag_id="email_orders_generator",
        wait_for_completion=True,
        poke_interval=30,
        conf={"triggered_by": "fake_data_orchestrator"},
    )

    # ---------------------------
    # Task 2: Trigger database orders generator DAG
    # ---------------------------
    trigger_database_orders_generator = TriggerDagRunOperator(
        task_id="trigger_database_orders_generator",
        trigger_dag_id="database_orders_generator",
        wait_for_completion=True,
        poke_interval=30,
        conf={"triggered_by": "fake_data_orchestrator"},
    )


    # Define execution order:
    trigger_email_orders_generator >> trigger_database_orders_generator