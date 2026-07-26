-- Gold: summary of Consumer vs Corporate distinct order share by market
select
    market,
    count(distinct case when segment = 'Consumer' then order_id end)
        as consumer_orders,
    count(distinct case when segment = 'Corporate' then order_id end)
        as corporate_orders,
    count(distinct order_id) as total_orders,
    count(distinct case when segment = 'Consumer' then order_id end)
    * 1.0
    / nullif(count(distinct order_id), 0) as consumer_share,
    count(distinct case when segment = 'Corporate' then order_id end)
    * 1.0
    / nullif(count(distinct order_id), 0) as corporate_share
from {{ ref('silver_ecom_sales') }}
group by market
order by total_orders desc
