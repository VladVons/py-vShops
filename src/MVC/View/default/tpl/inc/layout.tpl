<!doctype html>
<!--
Author:      VladVons
License:     GNU, see LICENSE for more details
-->
<html>
    <head>
        <link rel="stylesheet" href="/default/css/style.css?q=3.2" type="text/css">
        <meta charset="UTF-8">
        <title>{{ out.title }}</title>
        <!--layout.tpl head begin-->{% block head %}{% endblock %}<!--layout.tpl head end-->
    </head>
    <body>
        <h3><a href="/">Home</a>/{{ out.title }}</h3>
        <div id="content">
            <!--layout.tpl begin-->{% block content %}{% endblock %}<!--layout.tpl end-->
        </div>
        <div class="space"/>
        <div id="footer" class="app-footer">
            <a href="{{ out.info.get('home') }}">{{ '%s, %s, %s' % (out.info.get('home'), out.info.get('app_ver'), out.info.get('app_date')) }}</a>
        </div>
    </body>
</html>
