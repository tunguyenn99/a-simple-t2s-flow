-- Silver: clean and type-normalize customer data
with raw as (
    select *
    from {{ ref('bronze_customer') }}
)

select
    customer_id,
    gender,
    occupation,
    segment,
    country,
    city,
    try_cast(created_at as timestamp) as created_at,
    try_cast(updated_at as timestamp) as updated_at
from raw
