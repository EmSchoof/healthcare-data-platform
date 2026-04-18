WITH source AS (
    SELECT
        raw_record
    FROM {{ source('raw', 'fhir_patients') }}
),

final AS (
    SELECT
        raw_record:id::string AS patient_id,
        raw_record:resourceType::string AS resource_type,
        raw_record:gender::string AS gender,
        raw_record:birthDate::date AS birth_date,
        raw_record:name[0]:family::string AS lASt_name,
        raw_record:name[0]:given[0]::string AS first_name,
        raw_record:address[0]:city::string AS city,
        raw_record:address[0]:state::string AS state,
        raw_record:address[0]:postalCode::string AS postal_code,
        raw_record:identifier[0]:value::string AS mrn
    FROM source
)
SELECT * FROM final