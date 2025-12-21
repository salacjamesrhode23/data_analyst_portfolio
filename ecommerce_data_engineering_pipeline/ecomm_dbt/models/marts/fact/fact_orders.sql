{{ config(materialized='table') }}

with orders as (
    select
        ORDER_NUMBER,
        CUSTOMER_NAME,
        PRODUCT_SKU,
        QUANTITY,
        UNIT_PRICE,
        LINE_TOTAL,
        ORDER_DATE,
        PAYMENT_DATE,
        PAYMENT_METHOD,
        PAYMENT_REFERENCE,
        SOURCE
    from {{ ref('int_orders') }}
),

customers as (
    select
        CUSTOMER_ID,
        CUSTOMER_NAME
    from {{ ref('int_customers') }}
),

products as (
    select
        PRODUCT_ID,
        PRODUCT_SKU
    from {{ ref('int_products') }}
)

select

    o.ORDER_NUMBER,
    c.CUSTOMER_ID,
    p.PRODUCT_ID,
    
    o.QUANTITY,
    o.UNIT_PRICE,
    o.LINE_TOTAL,
    o.ORDER_DATE,
    o.PAYMENT_DATE,
    o.PAYMENT_METHOD,
    o.PAYMENT_REFERENCE,
    o.SOURCE

from orders o
left join customers c
    on o.CUSTOMER_NAME = c.CUSTOMER_NAME
left join products p
    on o.PRODUCT_SKU = p.PRODUCT_SKU
order by o.ORDER_DATE, c.CUSTOMER_ID, p.PRODUCT_ID
