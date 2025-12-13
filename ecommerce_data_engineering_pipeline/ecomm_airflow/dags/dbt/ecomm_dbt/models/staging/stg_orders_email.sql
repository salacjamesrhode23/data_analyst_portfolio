{{ config(materialized='view') }}

SELECT
-- Names and descriptive fields
  CAST(CUSTOMER AS STRING) AS CUSTOMER_NAME,
  CAST(PRODUCT AS STRING) AS PRODUCT_NAME,
  CAST(SKU AS STRING) AS PRODUCT_SKU,
  
  -- Numeric fields
  CAST(QTY AS INTEGER) AS QUANTITY,
  CAST(PRICE AS STRING) AS UNIT_PRICE,
  CAST(LINE_TOTAL AS STRING) AS LINE_TOTAL,
  CAST(TOTAL_AMOUNT AS STRING) AS TOTAL_AMOUNT,
  
  -- Dates and timestamps
  CAST(ORDER_DATE AS TIMESTAMP_NTZ) AS ORDER_DATE,
  CAST(PAYMENT_DATE AS TIMESTAMP_NTZ) AS PAYMENT_DATE,
  CAST(EMAIL_TIMESTAMP AS TIMESTAMP_NTZ) AS EMAIL_TIMESTAMP,
  
  -- Status/metadata
  CAST(PAYMENT_METHOD AS STRING) AS PAYMENT_METHOD,
  CAST(PAYMENT_REFERENCE AS STRING) AS PAYMENT_REFERENCE

FROM {{ source('raw_data', 'email_orders') }}

-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}
