# import modules
import os
import json
import snowflake.connector

# connect var to Snowflake demo db
conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA")
)
cursor = conn.cursor()

# load demo patient data into Snowflake demo db
def load_fhir_json(file_path):
    with open(file_path, "r") as f:
        patients = json.load(f)

    for patient in patients:
        cursor.execute(
            """
            INSERT INTO raw_fhir_patient (ingestion_ts, payload)
            SELECT CURRENT_TIMESTAMP, PARSE_JSON(%s)
            """,
            (json.dumps(patient),)
        )

    print(f"Loaded {len(patients)} records")

if __name__ == "__main__":
    load_fhir_json("../../data/sample_fhir.json")