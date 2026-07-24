-- Gold: VIP churn risk signals based on recency and order history
{{ churn_risk(
    ref('silver_ecom_sales'),
    'customer_id',
    'order_date',
    'revenue',
    5
) }}
