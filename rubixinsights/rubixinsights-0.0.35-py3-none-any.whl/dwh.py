from jinja2 import Template


def create_postgres_insert_sql(render_parameters):
    sql = """
    WITH processed_raw_{{channel}}_{{table_name}} AS (
        SELECT
            {%- for processed_column, column_alias in processed_columns.items() %}
            {{processed_column}} AS {{column_alias}}
            {%- if not loop.last -%}
                ,
            {%- endif -%}
            {%- endfor %}
        FROM raw.raw_{{channel}}_{{table_name}}
    )
    INSERT INTO
    {{channel}}.{{table_name}} (
        {%- for column in processed_columns.values() %}
        {{column}}
        {%- if not loop.last -%}
            ,
        {%- endif -%}
        {%- endfor %}
    )
    SELECT
    DISTINCT ON ({% for i in dimensions %}{{i}}{%- if not loop.last -%},{%- endif -%}{% endfor %}) * FROM processed_raw_{{channel}}_{{table_name}}
    ON CONFLICT ({% for i in dimensions %}{{i}}{%- if not loop.last -%},{%- endif -%}{% endfor %}) DO UPDATE SET
        {%- for metric in metrics %}
        {{metric}} = excluded.{{metric}}
        {%- if not loop.last -%}
            ,
        {%- endif -%}
        {%- endfor %}
    ;
    """
    return Template(sql).render(render_parameters)
