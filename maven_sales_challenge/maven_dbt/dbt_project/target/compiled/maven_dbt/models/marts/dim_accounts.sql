

with stg_accounts as (
    select
        account,
        sector
    from "mavensales_db"."analytics"."stg_accounts"
)

select
    md5(cast(coalesce(cast(account as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as account_id,
    account,
    sector
from stg_accounts