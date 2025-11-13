-- Use the `ref` function to select from other models

select *
from `de-project-nyc-taxi`.`analytics`.`my_first_dbt_model`
where id = 1