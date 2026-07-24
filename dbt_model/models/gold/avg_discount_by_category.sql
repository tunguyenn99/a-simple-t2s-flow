-- Gold: average discount by category
select
    category,
    avg(discount) as avg_discount
from {{ ref('silver_ecom_sales') }}
group by category
order by avg_discount desc
