{{ config(materialized='table') }}

with stg_customers as (
    select
        *
    from {{ ref('stg_customers') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['CUSTOMER_NAME', 'EMAIL']) }} as CUSTOMER_ID,
    CUSTOMER_NAME,
    EMAIL,
    STREET_ADDRESS,
    CITY,
    PROVINCE,
    ZIP,
    PHONE
from stg_customers

