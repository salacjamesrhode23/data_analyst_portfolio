
  create view "mavensales_db"."analytics"."stg_sales_pipeline__dbt_tmp"
    
    
  as (
    

select
    md5(cast(coalesce(cast(opportunity_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT))  as opportunity_id,
    cast(sales_agent as text)   as sales_agent,
    cast(
    case
        when lower(trim(product)) = 'gtxpro' then 'GTX Pro'
        else product
    end
 as text)   as product,
    cast(account as text)   as account,
    cast(deal_stage as text)    as deal_stage,
    cast(engage_date as date)   as engage_date,
    cast(close_date as date)    as close_date,
    cast(close_value as numeric(12,2))  as close_value
from "mavensales_db"."public"."sales_pipeline"
where account is not null
    and sales_agent is not null
    and product is not null
  );