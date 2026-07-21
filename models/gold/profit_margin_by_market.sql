-- Gold: profit margin by market
select
    market,
    {{ safe_divide('sum(profit)', 'sum(revenue)', 'null') }} as profit_margin
from {{ ref('silver_ecom_sales') }}
group by market
having sum(revenue) > 0
order by profit_margin desc
