-- Gold: top 3 profit-generating products in each category
with ranked as (
    select
        s.category,
        s.product_id,
        p.product_name,
        sum(s.profit) as total_profit,
        row_number() over (
            partition by s.category
            order by sum(s.profit) desc
        ) as rank
    from {{ ref('silver_ecom_sales') }} as s
    left join {{ ref('silver_product') }} as p
        on s.product_id = p.product_id
    group by s.category, s.product_id, p.product_name
)

select *
from ranked
where rank <= 3
order by category, rank
