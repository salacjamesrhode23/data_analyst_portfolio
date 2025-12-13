{{ config(materialized='table') }}

with int_customers as (
    select
        *
    from {{ ref('int_customers') }}
)

select
    CUSTOMER_ID,
    CUSTOMER_NAME,
    EMAIL,
    STREET_ADDRESS,
    CITY,
    PROVINCE,
    ZIP,
    PHONE
from int_customers

