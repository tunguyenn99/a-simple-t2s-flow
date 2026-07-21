{% macro safe_divide(numerator, denominator, zero_value='null') %}
case when {{ denominator }} is null or {{ denominator }} = 0 then {{ zero_value }} else {{ numerator }} / {{ denominator }} end
{% endmacro %}
