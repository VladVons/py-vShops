{% extends "theme1/tpl/inc/layout.tpl" %}

{% block content %}
<!--about.tpl begin-->
<br> theme1 !<br>
{% autoescape false%}
{{ out.data.info }}
{% endautoescape%}
<!--about.tpl end-->
{% endblock %}
