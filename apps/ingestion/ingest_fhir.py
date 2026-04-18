# import modules
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import snowflake.connector
from dotenv import load_dotenv
load_dotenv()
import json
import os

# dynamically load passkey
with open("rsa_key.p8", "rb") as key_file:
    p_key = serialization.load_pem_private_key(
        key_file.read(),
        password=os.getenv("SNOWFLAKE_PASSKEY_ENCRYPT").encode(),
        backend=default_backend()
    )

pkb = p_key.private_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

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