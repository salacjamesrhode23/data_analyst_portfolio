{{ config(materialized='table') }}

SELECT DISTINCT
    datetime_id,
    EXTRACT(HOUR FROM timestamp) AS hour,
    EXTRACT(DAY FROM timestamp)  AS day,
    TO_CHAR(timestamp, 'Day') AS day_name,
    EXTRACT(WEEK FROM timestamp) AS week
FROM {{ ref('int_transactions') }}
ORDER BY timestamp
