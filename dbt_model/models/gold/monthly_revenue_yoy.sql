-- Gold: revenue trend by month with YoY-style comparison
with monthly as (
    select
        date_trunc('month', order_date) as month_date,
        sum(revenue) as revenue
    from {{ ref('silver_ecom_sales') }}
    group by date_trunc('month', order_date)
)

select
    month_date,
    revenue,
    revenue - lag(revenue) over (order by month_date) as revenue_change,
    case
        when lag(revenue) over (order by month_date) is not null
            then (revenue / lag(revenue) over (order by month_date) - 1) * 100
    end as change_pct
from monthly
order by month_date
