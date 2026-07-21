-- Gold: total revenue and profit for the business
select
    sum(revenue) as total_revenue,
    sum(profit) as total_profit
from {{ ref('silver_ecom_sales') }}
