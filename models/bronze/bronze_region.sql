-- Bronze: raw region metadata loaded 1:1 from source
select *
from {{ source('raw', 'region') }}
