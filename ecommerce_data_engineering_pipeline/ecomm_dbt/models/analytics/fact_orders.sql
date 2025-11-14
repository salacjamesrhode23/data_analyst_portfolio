{{ config(materialized='table') }}

with orders_emails as (
    select
        quantity,       -- must be INT64 /
        unit_price,     -- remove Peso sign and convert to FLOAT64
        line_total,     -- remove Peso sign and convert to FLOAT64
        order_date,     -- must be date /
        payment_date    -- must be date /
    from {{ ref('stg_orders_emails') }}
)

select
    quantity,
    CAST({{ remove_peso_sign("unit_price") }} as FLOAT64) as unit_price,
    CAST({{ remove_peso_sign("line_total") }} as FLOAT64) as line_total,
    order_date,
    payment_date
from orders_emails