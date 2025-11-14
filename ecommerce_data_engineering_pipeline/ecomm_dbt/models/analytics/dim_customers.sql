{{ config(materialized='table') }}

with stg_customers as (
    select
        full_name,
        email,
        company,
        city,
        province,
        zip,
        phone
    from {{ ref('stg_customers') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['full_name']) }} as customer_id,
    full_name as customer_name,
    email,
    company,
    city,
    province,
    zip,
    phone
from stg_customers