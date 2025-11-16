{{ config(materialized='view') }}

SELECT
  CAST(billing_name AS STRING) AS customer_name,
  CAST(lineitem_name AS STRING) AS product_name,
  CAST(product_sku AS STRING) AS product_sku,
  CAST(lineitem_qty AS INT64) AS quantity,
  CAST(unit_price AS FLOAT64) AS unit_price,
  CAST(order_date AS DATETIME) AS order_date,
  CAST(payment_date as DATETIME) AS payment_date,
  CAST(payment_method AS STRING) AS payment_method
FROM {{ source('staging', 'raw_orders_postgres') }}

-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}