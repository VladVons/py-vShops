{% extends "default/tpl/inc/layout.tpl" %}

{% block content %}
<!--index.tpl begin-->
<table style="width:100%">
    {% for Key, Val in out.data.pages.items() %}
    <tr>
        <td><a href="{{Key}}">{{Val}}</a></td>
    </tr>
    {% endfor %}
    <tr>
        <td>&nbsp;</td>
    </tr>
    <tr>
        <td><a href="/form/login">login</a></td>
    </tr>
    <tr>
        <td><a href="/form/misc/about">about</a></td>
    </tr>
</table>
<!--index.tpl end-->
{% endblock %}
