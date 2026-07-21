{% macro duckdb_date_diff_days(start_date, end_date) %}
datediff('day', {{ start_date }}, {{ end_date }})
{% endmacro %}
