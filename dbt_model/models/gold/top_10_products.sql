-- Gold: top 10 products by unique order count
select
    s.product_id,
    p.product_name,
    count(distinct s.order_id) as order_count,
    sum(s.revenue) as revenue,
    sum(s.profit) as profit
from {{ ref('silver_ecom_sales') }} as s
left join {{ ref('silver_product') }} as p on s.product_id = p.product_id
group by s.product_id, p.product_name
order by order_count desc
limit 10
