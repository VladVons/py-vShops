{% extends "inc/layout1.tpl" %}

{% block content %}
<!--common/home.tpl begin-->
<br>default/tpl/common/home.tpl<br>
{% autoescape false%}
{{ out.data.info }}
{% endautoescape%}
<!--common/home.tpl end-->
{% endblock %}
