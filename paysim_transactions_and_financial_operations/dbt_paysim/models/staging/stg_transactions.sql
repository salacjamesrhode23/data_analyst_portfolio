{{ config(materialized='table') }}

SELECT
    CAST(transaction_id AS UUID)                        AS transaction_id,
    CAST(timestamp AS TIMESTAMP)                        AS timestamp,
    CAST(customer_id AS CHAR(11))                       AS customer_id,
    CAST(merchant_id AS CHAR(11))                       AS merchant_id,
    CAST(payment_method AS VARCHAR(10))                 AS payment_method,
    CAST(gateway AS VARCHAR(10))                        AS gateway,
    CAST(amount AS NUMERIC(12,2))                       AS amount,
    CAST(transaction_status AS VARCHAR(10))             AS transaction_status,
    CAST(processing_time_seconds AS DOUBLE PRECISION)   AS processing_time_seconds,
    CAST(country AS CHAR(2))                            AS country,
    CAST(device_type AS VARCHAR(10))                    AS device_type,
    CAST(is_fraud AS BOOLEAN)                           AS is_fraud,
    CAST(chargeback_flag AS BOOLEAN)                    AS chargeback_flag,
    CAST(refund_flag AS BOOLEAN)                        AS refund_flag
FROM {{ source('raw_data', 'transactions') }}