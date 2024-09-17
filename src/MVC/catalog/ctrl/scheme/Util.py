# Created: 2024.04.15
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import asyncio
import aiohttp
from bs4 import BeautifulSoup


def GetSoup(aData: str) -> BeautifulSoup:
    Res = BeautifulSoup(aData, 'lxml')
    if (len(Res) == 0):
        Res = BeautifulSoup(aData, 'html.parser')
    return Res

async def UrlGetData(aUrl: str) -> object:
    async def _GetUrlData(aHeaders: dict):
        async with aiohttp.ClientSession() as Session:
            try:
                async with Session.get(aUrl, headers=aHeaders) as Response:
                    Data = await Response.read()
                    Res = {'data': Data, 'status': Response.status}
            except Exception as E:
                Res = {'err': str(E), 'status': -1}
            return Res

    Headers = [
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
            'Accept-Language': 'uk'
        },
        {
            'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Accept-Language': 'uk'
        }
    ]

    for xHeader in Headers:
        Res = await _GetUrlData(xHeader)
        if (Res['status'] not in [403, 503]):
            break
        await asyncio.sleep(1.0)
    return Res
