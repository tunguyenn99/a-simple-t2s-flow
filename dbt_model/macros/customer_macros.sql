{% macro cross_market_customers(source_model, customer_col='customer_id', market_col='market') %}
with customer_markets as (
    select distinct {{ customer_col }}, {{ market_col }}
    from {{ source_model }}
)
select
    {{ customer_col }},
    count(distinct {{ market_col }}) as market_count,
    string_agg({{ market_col }}, ', ') as markets
from customer_markets
group by {{ customer_col }}
having count(distinct {{ market_col }}) > 1
order by market_count desc
{% endmacro %}

{% macro churn_risk(source_model, customer_col='customer_id', order_date_col='order_date', revenue_col='revenue', min_orders=5) %}
with customer_orders as (
    select
        {{ customer_col }},
        max({{ order_date_col }}) as last_order_date,
        count(*) as order_count,
        sum({{ revenue_col }}) as total_revenue
    from {{ source_model }}
    group by {{ customer_col }}
)
select
    {{ customer_col }},
    last_order_date,
    order_count,
    total_revenue,
    datediff('day', last_order_date, current_date) as days_since_last_order,
    case
        when datediff('day', last_order_date, current_date) > 90 then 'high'
        when datediff('day', last_order_date, current_date) > 45 then 'medium'
        else 'low'
    end as churn_risk
from customer_orders
where order_count >= {{ min_orders }}
order by days_since_last_order desc
{% endmacro %}

{% macro customer_rfm(source_model, customer_col='customer_id', order_date_col='order_date', revenue_col='revenue', recency_ntile=5, frequency_ntile=5, monetary_ntile=5) %}
with orders as (
    select
        {{ customer_col }},
        max({{ order_date_col }}) as last_order_date,
        count(*) as frequency,
        sum({{ revenue_col }}) as monetary
    from {{ source_model }}
    group by {{ customer_col }}
),
rfm as (
    select
        {{ customer_col }},
        datediff('day', last_order_date, current_date) as recency,
        frequency,
        monetary,
        ntile({{ recency_ntile }}) over(order by datediff('day', last_order_date, current_date)) as r_score,
        ntile({{ frequency_ntile }}) over(order by frequency desc) as f_score,
        ntile({{ monetary_ntile }}) over(order by monetary desc) as m_score
    from orders
)
select
    {{ customer_col }},
    recency,
    frequency,
    monetary,
    r_score,
    f_score,
    m_score,
    concat(r_score, f_score, m_score) as rfm_segment
from rfm
order by rfm_segment desc
{% endmacro %}
