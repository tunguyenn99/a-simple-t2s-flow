-- Silver: clean and type-normalize sales data
with raw as (
    select *
    from {{ ref('bronze_ecom_sales') }}
)

select
    order_id,
    customer_id,
    product_id,
    category,
    market,
    country,
    try_cast(quantity as integer) as quantity,
    try_cast(revenue as double) as revenue,
    try_cast(profit as double) as profit,
    try_cast(discount as double) as discount,
    try_cast(order_date as timestamp) as order_date
from raw
