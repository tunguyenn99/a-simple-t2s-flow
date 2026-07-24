-- Gold: customer RFM segmentation
{{ customer_rfm(
    ref('silver_ecom_sales'),
    'customer_id',
    'order_date',
    'revenue'
) }}
