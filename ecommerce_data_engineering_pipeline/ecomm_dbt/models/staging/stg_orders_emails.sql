{{ config(materialized='view') }}

SELECT
  CAST(customer AS STRING) AS customer_name,
  CAST(product AS STRING) AS product_name,
  CAST(sku AS STRING) AS product_sku,
  CAST(qty AS INT64) AS quantity,
  CAST(price AS STRING) AS unit_price,
  CAST(line_total AS STRING) as line_total,
  CAST(payment_method AS STRING) AS payment_method,
  CAST(payment_reference AS STRING) AS payment_reference,
  CAST(order_date AS DATETIME) AS order_date,
  CAST(payment_date as DATETIME) AS payment_date
FROM {{ source('staging', 'raw_orders_emails') }}
