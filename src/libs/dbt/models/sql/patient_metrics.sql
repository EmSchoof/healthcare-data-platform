SELECT
    state,
    COUNT(*) AS patient_count,
    AVG(DATEDIFF(year, birth_date, CURRENT_DATE)) AS avg_age
FROM {{ ref('stg_patient') }}
GROUP BY state