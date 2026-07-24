-- Silver: clean product catalog data
with raw as (
    select *
    from {{ ref('bronze_product') }}
)

select
    product_code as product_id,
    product as product_name,
    category,
    subcategory
from raw
