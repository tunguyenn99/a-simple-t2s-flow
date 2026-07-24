-- Silver: clean region metadata
with raw as (
    select *
    from {{ ref('bronze_region') }}
)

select
    region_code as region_id,
    city,
    state,
    country,
    region as region_name,
    market,
    try_cast(country_latitude as double) as country_latitude,
    try_cast(country_longitude as double) as country_longitude
from raw
