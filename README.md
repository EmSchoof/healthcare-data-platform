# Healthcare Data Platform (FHIR → Snowflake)

## Overview
This project simulates a healthcare data platform that ingests FHIR Patient data,
transforms it into analytics-ready tables, and exposes care management metrics.

## Architecture
- Ingestion: Python → Snowflake VARIANT
- Transformation: dbt (Medallion Architecture)
- Orchestration: Airflow
- Warehouse: Snowflake

## Data Flow
1. Load FHIR JSON into raw table
2. Normalize into structured staging layer
3. Aggregate into analytics marts

## Key Features
- Semi-structured ingestion (FHIR JSON)
- Incremental + deduplication logic
- Analytics-ready patient metrics

## Example Queries
- Patient count by state
- Average age distribution

## Future Enhancements
- Observations + Encounters
- Real-time ingestion (Snowpipe)
- Data quality checks (dbt tests)

### Pipeline Flow
- Ingest FHIR JSON into Snowflake stage
- Load into raw_fhir_patient (VARIANT)
- dbt transforms → patient_silver
- dbt builds marts → patient_metrics
- Airflow orchestrates daily runs
- BI / SQL queries consume metrics

### Demo Questions
- “How many patients per state?”
- “Average patient age by region?”
- “New patients ingested in last 24 hours?”