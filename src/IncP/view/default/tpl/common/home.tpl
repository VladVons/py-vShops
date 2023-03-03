{% extends "inc/layout.tpl" %}

{% block content %}
<!--common/home.tpl begin-->
{% autoescape false%}
{{ out.data.info }}
{% endautoescape%}
<!--common/home.tpl end-->
{% endblock %}
