{{ config(materialized='table') }}

with stg_products as (
    select
        *
    from {{ ref('stg_products') }}
)

select
    product_sku,
    product_name,
    product_description,
    product_category,
    unit_price,
    vendor,
    image_source
from stg_products