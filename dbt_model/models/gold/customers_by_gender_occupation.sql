-- Gold: customer distribution by gender and occupation
select
    gender,
    occupation,
    count(distinct customer_id) as customer_count
from {{ ref('silver_customer') }}
group by gender, occupation
order by customer_count desc
