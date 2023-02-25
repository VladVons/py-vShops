{% extends "default/tpl/inc/layout.tpl" %}

{% block content %}
<!--about.tpl content begin-->
{% autoescape false%}
{{ out.data.info }}
{% endautoescape%}
<!--about.tpl content end-->
{% endblock %}
