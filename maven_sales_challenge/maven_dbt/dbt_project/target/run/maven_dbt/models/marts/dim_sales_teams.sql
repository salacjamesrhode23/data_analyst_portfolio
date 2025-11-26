
  
    

  create  table "mavensales_db"."analytics"."dim_sales_teams__dbt_tmp"
  
  
    as
  
  (
    

with stg_sales_teams as (
    select
        sales_agent,
        manager
    from "mavensales_db"."analytics"."stg_sales_teams"
)

select
    md5(cast(coalesce(cast(sales_agent as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as sales_agent_id,
    sales_agent,
    manager
from stg_sales_teams
  );
  