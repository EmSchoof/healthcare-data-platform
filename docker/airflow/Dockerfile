FROM apache/airflow:2.8.0-python3.11

WORKDIR /opt/airflow

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dbt /opt/airflow/dbt
COPY src /opt/airflow/src

USER airflow
