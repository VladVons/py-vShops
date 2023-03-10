{% extends "inc/layout.tpl" %}

{% block content %}
<!--exit.tpl begin-->
<form method="post" action="{{ out.path }}">
    <input type="submit" name="btn_ok" value="restart server"/>
</form>
<!--exit.tpl end-->
{% endblock %}
