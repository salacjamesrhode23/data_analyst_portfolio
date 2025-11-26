

with stg_products as (
    select
        product,
        series,
        sales_price
    from "mavensales_db"."analytics"."stg_products"
)

select
    md5(cast(coalesce(cast(product as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as product_id,
    product,
    series,
    sales_price
from stg_products