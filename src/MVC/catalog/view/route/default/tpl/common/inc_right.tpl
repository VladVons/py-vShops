-= inc_right.tpl =-<br>
jinja2<br>
title: {{ title }}<br>
info: {{ info }}<br>
module: {{ module }}<br>
modules: {{ modules }}<br>
<br>
{% for module in modules['inc_right'] %}
  {{ module }}<br>
{% endfor %}
