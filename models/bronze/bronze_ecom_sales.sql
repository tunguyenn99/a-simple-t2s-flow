-- Bronze: raw e-commerce sales events loaded 1:1 from source
select *
from {{ source('raw', 'ecom_sales') }}
