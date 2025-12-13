{{ config(materialized='table') }}

with int_products as (
    select
        *
    from {{ ref('int_products') }}
)

select
    PRODUCT_ID,
    PRODUCT_NAME,
    PRODUCT_DESCRIPTION,
    PRODUCT_CATEGORY,
    UNIT_PRICE,
    VENDOR,
    IMAGE_SRC
from int_products
