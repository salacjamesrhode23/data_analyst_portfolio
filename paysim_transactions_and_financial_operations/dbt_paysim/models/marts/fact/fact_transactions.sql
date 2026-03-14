{{ config(materialized='table') }}

SELECT
    transaction_id,
    datetime_id,
    timestamp,
    customer_id,
    merchant_id,
    payment_method,
    gateway,
    amount,
    transaction_status,
    processing_time_seconds,
    country,
    device_type,
    is_fraud,
    chargeback_flag,
    refund_flag
FROM {{ ref('int_transactions') }}