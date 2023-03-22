=- inc_right.tpl =-<br>
jinja2<br>
info: {{ out.data.info }}<br>
modules: {{ out.data.modules }}<br>

{% for module in modules %}
  {{ module }}<br>
{% endfor %}
