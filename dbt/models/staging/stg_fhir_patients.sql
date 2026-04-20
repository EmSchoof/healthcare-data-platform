WITH source AS (
    SELECT
        raw_payload
    FROM {{ source('raw', 'raw_fhir_patients') }}
),

final AS (
    SELECT
        raw_payload:id::string AS patient_id,
        raw_payload:resourceType::string AS resource_type,
        raw_payload:gender::string AS gender,
        raw_payload:birthDate::date AS birth_date,
        raw_payload:name[0]:family::string AS lASt_name,
        raw_payload:name[0]:given[0]::string AS first_name,
        raw_payload:address[0]:city::string AS city,
        raw_payload:address[0]:state::string AS state,
        raw_payload:address[0]:postalCode::string AS postal_code,
        raw_payload:identifier[0]:value::string AS mrn
    FROM source
)
SELECT * FROM final