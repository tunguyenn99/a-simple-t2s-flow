-- Bronze: raw product catalog loaded 1:1 from source
select *
from {{ source('raw', 'product') }}
