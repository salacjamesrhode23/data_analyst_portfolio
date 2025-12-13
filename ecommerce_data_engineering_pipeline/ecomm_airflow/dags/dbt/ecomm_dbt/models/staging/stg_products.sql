{{ config(materialized='view') }}

SELECT
  -- Primary identifiers
  CAST(PRODUCT_SKU AS STRING) AS PRODUCT_SKU,
  
  -- Names and descriptive fields
  CAST(TITLE AS STRING) AS PRODUCT_NAME,
  CAST(PRODUCT_DESCRIPTION AS STRING) AS PRODUCT_DESCRIPTION,
  CAST(PRODUCT_CATEGORY AS STRING) AS PRODUCT_CATEGORY,
  CAST(VENDOR AS STRING) AS VENDOR,
  
  -- Numeric fields
  CAST(UNIT_PRICE AS FLOAT) AS UNIT_PRICE,
  
  -- Less-structured fields
  CAST(IMAGE_SRC AS STRING) AS IMAGE_SRC

FROM {{ source('raw_data', 'products') }}
