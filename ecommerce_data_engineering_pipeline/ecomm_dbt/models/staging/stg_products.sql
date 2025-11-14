{{ config(materialized='view') }}

SELECT
  CAST(`Image Src` AS STRING) AS image_source,
  CAST(`Product Category` AS STRING) AS product_category,
  CAST(`Product Description` AS STRING) AS product_description,
  CAST(Title AS STRING) AS product_name,
  CAST(`Unit Price` AS FLOAT64) AS unit_price,
  CAST(Vendor AS STRING) AS vendor
FROM {{ source('staging', 'raw_products') }}
