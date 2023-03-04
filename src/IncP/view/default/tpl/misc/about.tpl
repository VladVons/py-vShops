{% extends "inc/layout.tpl" %}

{% block content %}
<!--about.tpl begin-->
{% autoescape false%}
{{ out.data.info }}
{% endautoescape%}
<!--about.tpl end-->
{% endblock %}
