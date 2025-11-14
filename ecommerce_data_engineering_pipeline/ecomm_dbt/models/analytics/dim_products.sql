{{ config(materialized='table') }}

with stg_products as (
    select
        product_name,
        product_description,
        product_category,
        unit_price,
        vendor,
        image_source
    from {{ ref('stg_products') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['product_name']) }} as product_id,
    product_name,
    product_description,
    product_category,
    unit_price,
    vendor,
    image_source
from stg_products