# make sure Snowflake DB table exists prior to apo call
def ensure_fhir_patients_table(conn, cur) -> None:
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS raw_fhir_patients (
                resource_type STRING,
                patient_id STRING,
                first_name STRING,
                last_name STRING,
                gender STRING,
                birth_date DATE,
                city STRING,
                state STRING,
                postal_code STRING,
                country STRING,
                identifier_system STRING,
                identifier_value STRING,
                raw_payload VARIANT,
                ingested_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    finally:
        print("Raw FHIR Patients Table Confirmed in Snowflake.")