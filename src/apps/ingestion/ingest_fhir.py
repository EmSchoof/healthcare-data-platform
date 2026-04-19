from dotenv import load_dotenv
from src.libs.utils.snowflake_conn import connect_to_snowflake
import json

load_dotenv()

# insert raw FHIR demo patients into demo Snowflake db
def insert_fhir_patients(json_path: str):
    conn, cur = connect_to_snowflake()

    try:
        # optional: create table first
        cur.execute("""
            CREATE TABLE IF NOT EXISTS fhir_patients (
                resource_type       STRING,
                patient_id          STRING,
                family_name         STRING,
                given_name          STRING,
                gender              STRING,
                birth_date          DATE,
                city                STRING,
                state               STRING,
                postal_code         STRING,
                country             STRING,
                identifier_system   STRING,
                identifier_value    STRING,
                raw_payload         VARIANT,
                ingested_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP,
                source_file STRING
            )
        """)

        with open(json_path, "r", encoding="utf-8") as f:
            patients = json.load(f)

        rows = []
        for patient in patients:
            name0 = patient.get("name", [{}])[0] if patient.get("name") else {}
            address0 = patient.get("address", [{}])[0] if patient.get("address") else {}
            identifier0 = patient.get("identifier", [{}])[0] if patient.get("identifier") else {}

            rows.append((
                patient.get("resourceType"),
                patient.get("id"),
                name0.get("family"),
                (name0.get("given") or [None])[0],
                patient.get("gender"),
                patient.get("birthDate"),
                address0.get("city"),
                address0.get("state"),
                address0.get("postalCode"),
                address0.get("country"),
                identifier0.get("system"),
                identifier0.get("value"),
                json.dumps(patient),
            ))

        insert_sql = """
            INSERT INTO fhir_patients (
                resource_type,
                patient_id,
                family_name,
                given_name,
                gender,
                birth_date,
                city,
                state,
                postal_code,
                country,
                identifier_system,
                identifier_value,
                raw_payload
            )
            SELECT
                column1,
                column2,
                column3,
                column4,
                column5,
                column6,
                column7,
                column8,
                column9,
                column10,
                column11,
                column12,
                PARSE_JSON(column13)
            FROM VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """

        # execute cmds in Snowflake
        cur.executemany(insert_sql, rows)
        conn.commit()

        print(f"Loaded {len(rows)} records into fhir_patients")

    except Exception as e:
        conn.rollback()
        print(f"Error loading FHIR patients: {e}")
        raise

    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    insert_fhir_patients("src/data/sample_fhir.json")