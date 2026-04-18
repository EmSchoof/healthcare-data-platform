CREATE DATABASE healthcare;
CREATE SCHEMA healthcare.raw;
CREATE SCHEMA healthcare.silver;
CREATE SCHEMA healthcare.mart;

CREATE OR REPLACE TABLE healthcare.raw.raw_fhir_patient (
    ingestion_ts TIMESTAMP,
    payload VARIANT
);