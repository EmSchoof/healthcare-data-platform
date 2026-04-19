# import modules for airflow implementation
from __future__ import annotations
from datetime import datetime, timedelta
from pathlib import Path
import os

from airflow import DAG
from airflow.operators.bash import BashOperator

# Adjust this if your Airflow worker sees the repo at a different path.
REPO_ROOT = Path.cwd()
DBT_DIR_PATH = REPO_ROOT / "src" / "libs" / "dbt"

default_args = {
    "owner": "emschoof",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="healthcare_fhir_ingest_and_dbt",
    description="Run FHIR ingestion into Snowflake, then dbt transforms",
    default_args=default_args,
    start_date=datetime(2026, 4, 19),
    schedule="0 6 * * *",  # daily at 6:00 AM
    catchup=False,
    max_active_runs=1,
    tags=["healthcare", "fhir", "snowflake", "dbt"],
) as dag:

    ingest_fhir = BashOperator(
        task_id="ingest_fhir_to_snowflake",
        cwd=str(REPO_ROOT),
        bash_command="""
        set -euo pipefail
        python -m src.apps.ingestion.ingest_fhir
        """,
        env={
            **os.environ,
            "PYTHONPATH": str(REPO_ROOT),
        },
    )

    dbt_run = BashOperator(
        task_id="run_dbt_models",
        cwd=str(DBT_DIR_PATH),
        bash_command="""
        set -euo pipefail
        dbt run --target HEALTHCARE_DEMO
        """,
        env={
            **os.environ,
            "PYTHONPATH": str(REPO_ROOT),
        },
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        cwd=str(DBT_DIR_PATH),
        bash_command="set -euo pipefail && dbt test --target HEALTHCARE_DEMO",
        env={**os.environ, "PYTHONPATH": str(REPO_ROOT)},
    )

    ingest_fhir >> dbt_run >> dbt_test