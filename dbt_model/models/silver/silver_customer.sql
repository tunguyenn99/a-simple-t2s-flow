-- depends_on: {{ ref('bronze_customer') }}
-- Silver: clean and type-normalize customer data
with raw as (
    select *
    from {{ ref('bronze_customer') }}
)

select
    customer_id,
    first_name,
    last_name,
    marital_status,
    gender,
    email_address,
    education_level,
    occupation,
    home_owner,
    concat(first_name, ' ', last_name) as full_name,
    try_cast(birth_date as date) as birth_date,
    try_cast(annual_income as double) as annual_income
from raw
