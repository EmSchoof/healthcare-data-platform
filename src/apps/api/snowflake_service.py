# import modules for Snowflake service
from __future__ import annotations
from typing import Any, Optional
from src.libs.utils.snowflake_conn import connect_to_snowflake

# create patient row from DEMO FHIR input data within Snowflake demo DB
def row_to_patient(row: tuple[Any, ...]) -> dict[str, Any]:
    (
        patient_id,
        first_name,
        last_name,
        gender,
        birth_date,
        city,
        state,
        postal_code,
        country,
        identifier_system,
        identifier_value,
    ) = row

    return {
        "resourceType": "Patient",
        "id": patient_id,
        "identifier": [
            {
                "system": identifier_system,
                "value": identifier_value,
            }
        ]
        if identifier_value
        else [],
        "name": [
            {
                "use": "official",
                "family": last_name,
                "given": [first_name] if first_name else [],
            }
        ],
        "gender": gender,
        "birthDate": str(birth_date) if birth_date else None,
        "address": [
            {
                "city": city,
                "state": state,
                "postalCode": postal_code,
                "country": country,
            }
        ],
    }

# write row to Snowflake DB by patient ID
def get_patient_by_id(patient_id: str) -> Optional[dict[str, Any]]:
    conn, cur = connect_to_snowflake()
    try:
        cur.execute(
            """
            SELECT
                patient_id,
                first_name,
                last_name,
                gender,
                birth_date,
                city,
                state,
                postal_code,
                country,
                identifier_system,
                identifier_value
            FROM raw_fhir_patients
            WHERE patient_id = %s
            """,
            (patient_id,),
        )
        row = cur.fetchone()
        return row_to_patient(row) if row else None
    finally:
        cur.close()
        conn.close()

# search patient ID to verify if row for patient already exists in Snowflake DB
def search_patients(identifier: Optional[str] = None, family: Optional[str] = None) -> list[dict[str, Any]]:
    conn, cur = connect_to_snowflake()
    try:
        sql = """
            SELECT
                patient_id,
                first_name,
                last_name,
                gender,
                birth_date,
                city,
                state,
                postal_code,
                country,
                identifier_system,
                identifier_value
            FROM raw_fhir_patients
            WHERE 1=1
        """
        params: list[Any] = []

        if identifier:
            sql += " AND identifier_value = %s"
            params.append(identifier)

        if family:
            sql += " AND last_name ILIKE %s"
            params.append(family)

        cur.execute(sql, tuple(params))
        rows = cur.fetchall()
        return [row_to_patient(row) for row in rows]
    finally:
        cur.close()
        conn.close()

# create new patient row if patient ID does not already exist in Snowflake DB, otherwise return existing patient data
def create_patient(patient: dict[str, Any]) -> dict[str, Any]:
    conn, cur = connect_to_snowflake()
    try:
        name0 = patient.get("name", [{}])[0]
        addr0 = patient.get("address", [{}])[0]
        ident0 = patient.get("identifier", [{}])[0]

        cur.execute(
            """
            INSERT INTO raw_fhir_patients(
                patient_id,
                first_name,
                last_name,
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
                PARSE_JSON(column12)
            FROM VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                patient["id"],
                (name0.get("given") or [None])[0],
                name0.get("family"),
                patient.get("gender"),
                patient.get("birthDate"),
                addr0.get("city"),
                addr0.get("state"),
                addr0.get("postalCode"),
                addr0.get("country"),
                ident0.get("system"),
                ident0.get("value"),
                str(patient).replace("'", '"'),
            ),
        )
        conn.commit()
        return patient
    finally:
        cur.close()
        conn.close()