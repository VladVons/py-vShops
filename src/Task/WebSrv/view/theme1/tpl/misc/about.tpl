{% extends "theme1/tpl/inc/layout.tpl" %}

{% block content %}
<!--about.tpl content begin-->
<br> theme1 !<br>
{% autoescape false%}
{{ out.data.info }}
{% endautoescape%}
<!--about.tpl content end-->
{% endblock %}
