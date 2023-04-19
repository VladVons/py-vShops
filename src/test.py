# Created: 2023.03.19
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#
# https://www.youtube.com/watch?v=bu5wXjz2KvU
# https://console.developers.google.com

import re
import time
import asyncio
import aiohttp
import gspread
#
from Inc.Misc.Request import TDownload
from Inc.DbList import TDbList


def Test_05():
    #Auth = '~/.config/gspread/service_account.json'
    gc = gspread.service_account()

    Url = 'https://docs.google.com/spreadsheets/d/1EIwjTitfj1_oyWS7ralnUCtq8ZH0g3DWBKq3gP4qrvo/edit#gid=782031503'
    sh = gc.open_by_url(Url)
    wsl = sh.worksheets()
    ws = sh.worksheet('MONITORS')
    print(ws.row_count, ws.col_count)
    Values = ws.get_all_values()

def Test_06():
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

def Test_07():
    import requests

    Url = 'https://images.prom.ua/4409017669_w640_h640_aromatizator-dlya-avtomobilya.jpg'
    for i in range(100):
        Data = requests.get(Url, stream=True)
        print(Data.headers['Content-length'])

async def Test_08():
    Url = 'https://images.prom.ua/4409017669_w640_h640_aromatizator-dlya-avtomobilya.jpg'
    #Url = 'https://speed.hetzner.de/1GB.bin'

    StartAt = time.time()
    Cnt = 25
    async with aiohttp.ClientSession() as session:
        for i in range(Cnt):
            async with session.get(Url) as response:
                #Data = await response.read()
                Len = response.headers['Content-Length']
                print(Len)
    print('done', round((time.time() - StartAt) / Cnt, 3))

async def Test_09():
    StartAt = time.time()

    Url = 'https://loremflickr.com/800/600/girl'
    Url = 'https://images.prom.ua/4409017669_w640_h640_aromatizator-dlya-avtomobilya.jpg'

    Cnt = 3
    Download = TDownload('Temp')
    Urls = [Url for x in range(Cnt)]
    #SaveAs = [f'girl_{i:02}.jpg' for i in range(Cnt)]
    SaveAs = None
    Res = await Download.Get(Urls, SaveAs)
    print('done', round((time.time() - StartAt) / Cnt, 3))


def Test_10():
    Data = [
        ['User5', 55, True, 5.67],
        ['User2', 22, True, 2.34],
        ['User6', 66, True, 6.78],
        ['User1', 11, False, 1.23],
        ['User3', 33, True, 3.45],
        ['User4', 44, True, 4.56],
        ['User5', 55, True, 5.55]
    ]

    Dbl1 = TDbList(
        ['User', 'Age', 'Male', 'Price'],
        Data
    )
    q1 = Dbl1.ExportStr(['User', 'Price'], '{}/{}')
    print(q1)

Test_10()

#asyncio.run(Test_09())
