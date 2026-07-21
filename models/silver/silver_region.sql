-- Silver: clean region metadata
with raw as (
    select *
    from {{ ref('bronze_region') }}
)

select
    region_id,
    market,
    country,
    region_name,
    try_cast(population as integer) as population
from raw
