=- inc_right.tpl =-<br>
jinja2<br>
title: {{ title }}<br>
info: {{ info }}<br>
modules: {{ modules }}<br>
{% for module in modules['inc_right'] %}
  {{ module }}<br>
{% endfor %}
