# import modules
from airflow.operators.bash import BashOperator
from airflow import DAG
from datetime import datetime

with DAG(
    dag_id="fhir_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    run_dbt = BashOperator(
        task_id="run_dbt_models",
        bash_command="cd ../../libs/dbt && dbt run"
    )