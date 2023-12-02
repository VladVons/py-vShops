from jinja2 import Template

data = {
    'pages': 2,
    'current': 10,
    'total': 12 
}


template = """
    {% set current_page = pagination.current %}
    {% set total_pages = pagination.total %}

    {% set inner_range = pagination.pages %}
    {% set outer_range = 1 %}

    {%- if current_page > 1 -%}
      1
    {% endif %}

    {%- if current_page > (outer_range + 1) -%}
      ...
    {% endif %}

    {%- for page in range([1, current_page - inner_range]|max, [total_pages, current_page + inner_range]|min + 1) -%}
      {%- if page == current_page -%}
        {{ page }}+
      {% else %}
        {{ page }}
      {% endif %}
    {% endfor %}

    {%- if current_page < (total_pages - outer_range) -%}
      ...
    {% endif %}

    {%- if current_page < total_pages -%}
      {{total_pages}}
    {% endif %}
"""


template1 = """
    {% if pagination.total <= pagination.pages %}
        {% for page in range(1, pagination.total + 1) %}
            {{page}}
        {% endfor %}
    {% else %}
        1
        {% for page in range([1,2,3] | min, pagination.total + 1) %}
            {{page}}
        {% endfor %}
        {{pagination.total}}
    {% endif %}

"""

template = Template(template)
output = template.render(pagination=data)
print(output)
