SELECT
    patient_id,
    mrn,
    first_name,
    last_name,
    gender,
    birth_date,
    city,
    state,
    postal_code
FROM {{ ref('stg_fhir_patients') }}