{{ config(materialized='table') }}

with stg_customers as (
    select
        *
    from {{ ref('stg_customers') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['customer_name']) }} as customer_id,
    customer_name,
    email,
    street_address,
    city,
    province,
    zip,
    phone
from stg_customers