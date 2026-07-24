-- Bronze: raw customer data loaded 1:1 from source
select *
from {{ source('raw', 'customer') }}
