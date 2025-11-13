

  create or replace view `de-project-nyc-taxi`.`analytics`.`my_second_dbt_model`
  OPTIONS()
  as -- Use the `ref` function to select from other models

select *
from `de-project-nyc-taxi`.`analytics`.`my_first_dbt_model`
where id = 1;

