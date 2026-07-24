-- Gold: product pairs frequently purchased together
{{ market_basket_pairs(
    ref('silver_ecom_sales'),
    'order_id',
    'product_id',
    20
) }}
