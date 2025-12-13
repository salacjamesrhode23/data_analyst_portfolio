{{ config(materialized='table') }}

with stg_products as (
    select
        *
    from {{ ref('stg_products') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['PRODUCT_SKU', 'VENDOR']) }} as PRODUCT_ID,
    PRODUCT_SKU,
    PRODUCT_NAME,
    PRODUCT_DESCRIPTION,
    PRODUCT_CATEGORY,
    UNIT_PRICE,
    VENDOR,
    IMAGE_SRC
from stg_products
