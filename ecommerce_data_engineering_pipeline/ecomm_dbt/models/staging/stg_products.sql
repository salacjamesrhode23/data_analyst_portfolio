{{ config(materialized='view') }}

SELECT
  CAST(`Product SKU` AS STRING) AS product_sku,
  CAST(Title AS STRING) AS product_name,
  CAST(`Product Description` AS STRING) AS product_description,
  CAST(`Product Category` AS STRING) AS product_category,
  CAST(`Unit Price` AS FLOAT64) AS unit_price,
  CAST(Vendor AS STRING) AS vendor,
  CAST(`Image Src` AS STRING) AS image_source,
FROM {{ source('staging', 'raw_products') }}
