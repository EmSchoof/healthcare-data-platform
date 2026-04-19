 # Healthcare Data Platform Demo

A small healthcare data engineering demo project that ingests synthetic FHIR Patient resources into Snowflake, transforms semi-structured records into analytics-ready models with dbt, and orchestrates the workflow with Airflow.

## Project Goal

This project demonstrates a production-shaped healthcare analytics pipeline:

- ingest synthetic FHIR Patient JSON data into Snowflake
- preserve the original resource payload in a raw semi-structured column
- transform raw records into clean warehouse models with dbt
- validate key data quality rules with dbt tests
- orchestrate ingestion and transformation with Airflow

_Credentials, local dbt profiles, Snowflake private keys, dbt artifacts, logs, and non-curated data extracts are intentionally excluded from version control._

## Tech Stack

- Python
- Snowflake
- dbt
- Airflow

## Current Functionality

### 1. Ingestion
Python loads synthetic FHIR Patient resources into Snowflake.

The raw table stores:
- structured patient fields for analytics
- the original FHIR payload in a Snowflake `VARIANT` column

### 2. Transformation
dbt transforms raw patient records into:
- `stg_fhir_patients`
- `dim_patients`
- `patient_summary`

### 3. Data Quality
dbt tests validate:
- `patient_id` is not null
- `patient_id` is unique in `dim_patients`
- `resource_type` must equal `Patient`

### 4. Orchestration
Airflow runs the pipeline in this order:
1. ingest FHIR JSON
2. run dbt models
3. run dbt tests

## Repository Structure

```text
src/
  apps/
    ingestion/
      ingest_fhir.py
  data/
    sample_fhir.json

dbt_project/
  dbt_project.yml
  models/
    sources.yml
    staging/
      stg_fhir_patients.sql
      staging.yml
    marts/
      dim_patients.sql
      patient_summary.sql
      marts.yml

airflow/
  dags/
    healthcare_data_platform_demo.py
 ```

### Demo Questions
- “How many patients per state?”
- “Average patient age by region?”
- “New patients ingested in last 24 hours?”