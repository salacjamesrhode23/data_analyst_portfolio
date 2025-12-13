{{ config(materialized='table') }}

with orders_email as (
    select
        CUSTOMER_NAME,  
        PRODUCT_NAME,            
        PRODUCT_SKU,
        QUANTITY,  
        cast({{ remove_peso_sign("UNIT_PRICE") }} as FLOAT) as UNIT_PRICE,
        cast({{ remove_peso_sign("LINE_TOTAL") }} as FLOAT) as LINE_TOTAL,
        {{ dbt_utils.generate_surrogate_key(['ORDER_DATE', 'CUSTOMER_NAME']) }} as ORDER_NUMBER,
        ORDER_DATE,
        PAYMENT_DATE,
        PAYMENT_METHOD,
        PAYMENT_REFERENCE,
        'email' as SOURCE
    from {{ ref('stg_orders_email') }}
),

orders_parquet as (
    select
        CUSTOMER_NAME,
        PRODUCT_NAME,
        PRODUCT_SKU,
        QUANTITY,
        UNIT_PRICE,
        CAST(QUANTITY * UNIT_PRICE AS FLOAT) as LINE_TOTAL,
        {{ dbt_utils.generate_surrogate_key(['ORDER_DATE', 'CUSTOMER_NAME']) }} as ORDER_NUMBER,
        ORDER_DATE,
        PAYMENT_DATE,
        PAYMENT_METHOD,
        PAYMENT_REFERENCE,
        'parquet' as SOURCE
    from {{ ref('stg_orders_parquet') }}
),

orders_database as (
    select
        CUSTOMER_NAME,
        PRODUCT_NAME,
        PRODUCT_SKU,
        QUANTITY,
        UNIT_PRICE,
        CAST(QUANTITY * UNIT_PRICE AS FLOAT) as LINE_TOTAL,
        {{ dbt_utils.generate_surrogate_key(['ORDER_DATE', 'CUSTOMER_NAME']) }} as ORDER_NUMBER,
        ORDER_DATE,
        PAYMENT_DATE,
        PAYMENT_METHOD,
        PAYMENT_REFERENCE,
        'database' as SOURCE
    from {{ ref('stg_orders_database') }}
)


select * from orders_email
union all
select * from orders_parquet
union all
select * from orders_database
