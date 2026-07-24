-- Silver: clean and type-normalize sales data
with raw as (
    select *
    from {{ ref('bronze_ecom_sales') }}
),

product as (
    select *
    from {{ ref('silver_product') }}
),

region as (
    select *
    from {{ ref('silver_region') }}
)

select
    s.order_id,
    s.customer_id,
    s.product_code as product_id,
    s.segment,
    p.category,
    p.subcategory,
    r.market,
    r.country,
    r.city,
    try_cast(s.quantity as integer) as quantity,
    try_cast(s.sales as double) as revenue,
    try_cast(s.profit as double) as profit,
    try_cast(s.discount as double) as discount,
    try_cast(s.order_date as timestamp) as order_date
from raw as s
left join product as p on s.product_code = p.product_id
left join region as r on s.region_code = r.region_id
