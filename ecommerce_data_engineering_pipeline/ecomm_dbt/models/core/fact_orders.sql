{{ config(materialized='table') }}

with orders_emails as (
    select
        customer_name,
        product_name,
        product_sku,
        quantity,       
        CAST({{ remove_peso_sign("unit_price") }} as FLOAT64) as unit_price,
        CAST({{ remove_peso_sign("line_total") }} as FLOAT64) as line_total,
        order_date,
        payment_date,
        payment_method
    from {{ ref('stg_orders_emails') }}
),

orders_faker as (
    select
        *
    from {{ ref('stg_orders_faker') }}
),

orders_postgres as (
    select
        *
    from {{ ref('stg_orders_postgres') }}
)

select 
    {{ dbt_utils.generate_surrogate_key(['customer_name', 'order_date']) }} as order_id,
    customer_name,
    product_name,
    product_sku,
    quantity,       
    unit_price,
    line_total,
    order_date,
    payment_date,
    payment_method
from orders_emails

union all 

select 
    {{ dbt_utils.generate_surrogate_key(['customer_name', 'order_date']) }} as order_id,
    customer_name,
    product_name,
    product_sku,
    quantity,       
    unit_price,
    CAST(quantity * unit_price AS FLOAT64) as line_total,
    order_date,
    payment_date,
    payment_method
from orders_faker

union all 

select 
    {{ dbt_utils.generate_surrogate_key(['customer_name', 'order_date']) }} as order_id,
    customer_name,
    product_name,
    product_sku,
    quantity,       
    unit_price,
    CAST(quantity * unit_price AS FLOAT64) as line_total,
    order_date,
    payment_date,
    payment_method
from orders_postgres

