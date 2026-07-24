{% macro market_basket_pairs(source_model, order_id_col='order_id', product_id_col='product_id', limit=20) %}
with order_products as (
    select distinct {{ order_id_col }}, {{ product_id_col }}
    from {{ source_model }}
),
pairs as (
    select
        a.{{ product_id_col }} as product_id_a,
        b.{{ product_id_col }} as product_id_b,
        count(*) as co_purchase_count
    from order_products a
    join order_products b
      on a.{{ order_id_col }} = b.{{ order_id_col }}
      and a.{{ product_id_col }} < b.{{ product_id_col }}
    group by 1, 2
)
select
    product_id_a,
    product_id_b,
    co_purchase_count
from pairs
order by co_purchase_count desc
limit {{ limit }}
{% endmacro %}
