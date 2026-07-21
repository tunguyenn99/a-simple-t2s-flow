-- Gold: revenue and profit by customer segment
select
    segment,
    sum(revenue) as revenue,
    sum(profit) as profit
from {{ ref('silver_ecom_sales') }}
group by segment
order by revenue desc
