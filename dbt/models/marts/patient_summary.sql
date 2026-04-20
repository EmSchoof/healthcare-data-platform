SELECT
    state,
    gender,
    count(*) AS patient_count
FROM {{ ref('dim_patients') }}
GROUP BY 1, 2