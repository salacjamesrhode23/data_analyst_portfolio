{{ config(materialized='table') }}

with orders as (
    select
        CUSTOMER_NAME,
        PRODUCT_SKU,
        QUANTITY,
        UNIT_PRICE,
        LINE_TOTAL,
        ORDER_NUMBER,
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
        CUSTOMER_NAME,
        EMAIL,
        STREET_ADDRESS,
        CITY,
        PROVINCE,
        ZIP,
        PHONE
    from {{ ref('int_customers') }}
),

products as (
    select
        PRODUCT_ID,
        PRODUCT_NAME,
        PRODUCT_SKU,
        PRODUCT_DESCRIPTION,
        PRODUCT_CATEGORY,
        VENDOR,
        IMAGE_SRC
    from {{ ref('int_products') }}
)

SELECT

    c.CUSTOMER_ID,
    c.CUSTOMER_NAME,
    c.EMAIL,
    c.STREET_ADDRESS,
    c.CITY,
    c.PROVINCE,
    c.ZIP,
    c.PHONE,
    
    p.PRODUCT_ID,
    p.PRODUCT_NAME,
    p.PRODUCT_DESCRIPTION,
    p.PRODUCT_CATEGORY,
    p.VENDOR,
    p.IMAGE_SRC,
    
    o.ORDER_NUMBER,
    o.QUANTITY,
    o.UNIT_PRICE,
    o.LINE_TOTAL,
    o.ORDER_DATE,
    o.PAYMENT_DATE,
    o.PAYMENT_METHOD,
    o.PAYMENT_REFERENCE,
    o.SOURCE

FROM orders o
LEFT JOIN customers c
    ON o.CUSTOMER_NAME = c.CUSTOMER_NAME
JOIN products p
    ON o.PRODUCT_SKU = p.PRODUCT_SKU
ORDER BY o.ORDER_DATE, c.CUSTOMER_NAME, p.PRODUCT_NAME