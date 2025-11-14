{{ config(materialized='view') }}

SELECT
  CAST(billing_name AS STRING) AS customer_name,
  CAST(lineitem_name AS STRING) AS product_name,
  CAST(product_sku AS STRING) AS product_sku,
  CAST(lineitem_qty AS INT64) AS quantity,
  CAST(unit_price AS STRING) AS unit_price,
  CAST(payment_method AS STRING) AS payment_method,
  CAST(payment_reference AS STRING) AS payment_reference,
  CAST(order_date AS DATE) AS order_date,
  CAST(payment_date as DATE) AS payment_date
FROM {{ source('staging', 'raw_orders_faker') }}
