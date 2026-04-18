WITH source AS (
    SELECT *
    FROM healthcare.raw.raw_fhir_patient
)

SELECT
    payload:id::STRING AS patient_id,
    payload:name[0].given[0]::STRING AS first_name,
    payload:name[0].family::STRING AS last_name,
    payload:gender::STRING AS gender,
    payload:birthDate::DATE AS birth_date,
    payload:address[0].city::STRING AS city,
    payload:address[0].state::STRING AS state,
    ingestion_ts

FROM source

QUALIFY ROW_NUMBER() OVER (
    PARTITION BY payload:id::STRING
    ORDER BY ingestion_ts DESC
) = 1