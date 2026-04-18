# import modules
from dotenv import load_dotenv
from src.libs.utils.snowflake_conn import connect_to_snowflake
load_dotenv()
import json

def open_snowflake_connection():
    conn, cur = connect_to_snowflake()
    return conn, cur

# load demo patient data into Snowflake demo db
def load_fhir_json(file_path,  cur):
    with open(file_path, "r") as f:
        patients = json.load(f)

    for patient in patients:
        cur.execute(
            """
            INSERT INTO raw_fhir_patient (ingestion_ts, payload)
            SELECT CURRENT_TIMESTAMP, PARSE_JSON(%s)
            """,
            (json.dumps(patient),)
        )

    print(f"Loaded {len(patients)} records")

if __name__ == "__main__":
    conn, cur = open_snowflake_connection()
    load_fhir_json("src/data/sample_fhir.json", cur)
    cur.close()
    conn.close()