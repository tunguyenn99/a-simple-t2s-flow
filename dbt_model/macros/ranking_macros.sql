{% macro top_n_by_partition(source_model, partition_by, group_by, metrics, order_by, top_n=3) %}
select *
from (
    select
        {{ group_by }},
        {{ metrics }},
        row_number() over(partition by {{ partition_by }} order by {{ order_by }}) as rank
    from {{ source_model }}
    group by {{ group_by }}
) ranked
where rank <= {{ top_n }}
{% endmacro %}
