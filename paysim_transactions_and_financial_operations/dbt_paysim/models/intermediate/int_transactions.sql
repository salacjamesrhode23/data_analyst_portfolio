{{ config(materialized='table') }}

SELECT
    transaction_id,
	CAST(TO_CHAR(timestamp, 'YYYYMMDDHH24') AS BIGINT) AS datetime_id,
    timestamp,
    customer_id,
    merchant_id,
    payment_method,
    gateway,
    amount,
    transaction_status,
    processing_time_seconds,
    CASE
		WHEN country = 'PH' THEN 'Philippines'
		WHEN country = 'SG' THEN 'Singapore'
		WHEN country = 'MY' THEN 'Malaysia'
		WHEN country = 'ID' THEN 'Indonesia'
		ELSE 'Unknown'
	END AS country,
    device_type,
    is_fraud,
    chargeback_flag,
    refund_flag
FROM {{ ref('stg_transactions') }}