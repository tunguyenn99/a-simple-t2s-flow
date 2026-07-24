-- Gold: summary of Consumer vs Corporate share by market
select
    market,
    sum(case when segment = 'Consumer' then 1 else 0 end) as consumer_orders,
    sum(case when segment = 'Corporate' then 1 else 0 end) as corporate_orders,
    count(*) as total_orders,
    sum(case when segment = 'Consumer' then 1 else 0 end)
    * 1.0
    / nullif(count(*), 0) as consumer_share,
    sum(case when segment = 'Corporate' then 1 else 0 end)
    * 1.0
    / nullif(count(*), 0) as corporate_share
from {{ ref('silver_ecom_sales') }}
group by market
order by total_orders desc
