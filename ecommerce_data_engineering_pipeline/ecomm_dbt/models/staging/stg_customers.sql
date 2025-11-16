{{ config(materialized='view') }}

SELECT
  CAST(`Full Name` AS STRING) AS customer_name,
  CAST(Email AS STRING) AS email,
  CAST(`Address Company` AS STRING) AS street_address,
  CAST(`Address City` AS STRING) AS city,
  CAST(`Address Province` AS STRING) AS province,
  CAST(`Address Zip` AS STRING) AS zip,
  CAST(Phone AS STRING) AS phone
FROM {{ source('staging', 'raw_customers') }}
