-- Silver: clean product catalog data
with raw as (
    select *
    from {{ ref('bronze_product') }}
)

select
    product_id,
    product_name,
    category,
    try_cast(list_price as double) as list_price,
    try_cast(cost as double) as product_cost
from raw
