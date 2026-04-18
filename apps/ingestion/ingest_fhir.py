import json
import snowflake.connector

# Replace with env vars in real setup
conn = snowflake.connector.connect(
    user="YOUR_USER",
    password="YOUR_PASSWORD",
    account="YOUR_ACCOUNT",
    warehouse="COMPUTE_WH",
    database="HEALTHCARE",
    schema="RAW"
)

cursor = conn.cursor()

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