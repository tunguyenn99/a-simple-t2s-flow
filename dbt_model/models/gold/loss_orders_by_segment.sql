-- Gold: count of distinct loss orders by segment
select
    segment,
    count(distinct order_id) as loss_order_count
from {{ ref('silver_ecom_sales') }}
where profit < 0
group by segment
order by loss_order_count desc
