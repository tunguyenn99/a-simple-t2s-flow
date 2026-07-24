-- Gold: top 15 countries by revenue
select
    country,
    sum(revenue) as revenue,
    count(distinct customer_id) as unique_customers
from {{ ref('silver_ecom_sales') }}
group by country
order by revenue desc
limit 15
