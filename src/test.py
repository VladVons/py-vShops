# Created: 2023.03.19
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#
# https://www.youtube.com/watch?v=bu5wXjz2KvU
# https://console.developers.google.com

import re
import gspread


def Test_05():
    #Auth = '~/.config/gspread/service_account.json'
    gc = gspread.service_account()

    Url = 'https://docs.google.com/spreadsheets/d/1EIwjTitfj1_oyWS7ralnUCtq8ZH0g3DWBKq3gP4qrvo/edit#gid=782031503'
    sh = gc.open_by_url(Url)
    wsl = sh.worksheets()
    ws = sh.worksheet('MONITORS')
    print(ws.row_count, ws.col_count)
    Values = ws.get_all_values()


Source = '''
    {%  extends  "inc/layout1.j2"  %}
    {% include './header_head.j2'%}
    {% block head %}
    {% endblock  %}
'''

#self.ReVar = re.compile(r'''[{]{1,2}%?\s*([a-z-_]+)\s*['"]?([^'"}]*)['"]*\s*%?[}]{1,2}''')
ReMacro = re.compile(r'''\{%\s*(\w+)\s*['"]?([\w/.]+)['"]?\s*%\}''')
Vars = ReMacro.findall(Source)
print(Vars)
