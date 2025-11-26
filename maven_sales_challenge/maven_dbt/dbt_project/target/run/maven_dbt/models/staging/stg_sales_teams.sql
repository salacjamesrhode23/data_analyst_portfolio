
  create view "mavensales_db"."analytics"."stg_sales_teams__dbt_tmp"
    
    
  as (
    

select
    cast(sales_agent as text)   as sales_agent,
    cast(manager as text)    as manager,
    cast(regional_office as text)  regional_office
from "mavensales_db"."public"."sales_teams"
  );