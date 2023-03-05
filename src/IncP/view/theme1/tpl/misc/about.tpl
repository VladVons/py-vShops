{% extends "inc/layout.tpl" %}

{% block content %}
<br>theme1/tpl/misc/about.tpl<br>
<!--about.tpl begin-->
{% autoescape false%}
{{ out.data.info }}
{% endautoescape%}
<!--about.tpl end-->
{% endblock %}
