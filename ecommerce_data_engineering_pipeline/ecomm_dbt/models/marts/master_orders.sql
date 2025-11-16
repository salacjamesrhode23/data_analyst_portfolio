{{ config(materialized='table') }}

with orders as (
    select
        *
    from {{ ref('fact_orders') }}
),

customers as (
    select
        *
    from {{ ref('dim_customers') }}
),

products as (
    select
        *
    from {{ ref('dim_products') }}
)

SELECT
    o.order_id,
    o.quantity,
    o.unit_price,
    o.line_total,
    o.order_date,
    o.payment_date,
    o.payment_method,

    c.customer_id,
    c.customer_name,
    c.email,
    c.street_address,
    c.city,
    c.province,
    c.zip,
    c.phone,

    p.product_sku,
    p.product_name,
    p.product_description,
    p.product_category,
    p.unit_price as product_unit_price,
    p.vendor,
    p.image_source
FROM orders o
LEFT JOIN customers c
    ON o.customer_name = c.customer_name
LEFT JOIN products p
    ON o.product_name = p.product_name

