{% extends "inc/layout.tpl" %}

{% block content %}
default/tpl/misc/about.tpl<br>
<br>
<!--about.tpl begin-->
{% autoescape false%}
{{ out.data.info }}
{% endautoescape%}
<!--about.tpl end-->
{% endblock %}
