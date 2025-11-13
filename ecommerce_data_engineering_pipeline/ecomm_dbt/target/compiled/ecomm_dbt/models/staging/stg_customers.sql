

SELECT
  CAST(`Address City` AS STRING) AS city,
  CAST(`Address Company` AS STRING) AS company,
  CAST(`Address Province` AS STRING) AS province,
  CAST(`Address Zip` AS STRING) AS zip,
  CAST(Email AS STRING) AS email,
  CAST(`First Name` AS STRING) AS first_name,
  CAST(`Full Name` AS STRING) AS full_name,
  CAST(`Last Name` AS STRING) AS last_name,
  CAST(Phone AS STRING) AS phone
FROM `de-project-nyc-taxi`.`staging`.`stg_api_customers`