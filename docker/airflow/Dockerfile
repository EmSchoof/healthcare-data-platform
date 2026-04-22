FROM apache/airflow:2.8.0-python3.11

WORKDIR /opt/airflow

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Airflow configs, DAGs, and dbt profiles
COPY airflow/dags /opt/airflow/dags
COPY airflow/config /opt/airflow/config
COPY airflow/dbt_profiles /opt/airflow/dbt_profiles

# Copy dbt and source code
COPY dbt /opt/airflow/dbt
COPY src /opt/airflow/src

# Set dbt profiles directory
ENV DBT_PROFILES_DIR=/opt/airflow/dbt_profiles

USER airflow
