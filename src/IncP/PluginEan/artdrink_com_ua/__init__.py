# Created: 2023.06.02
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
import asyncio
import aiohttp
from bs4 import BeautifulSoup
#
from Inc.Ean import TEan
from IncP.Log import Log
from .. import TParserBase


class TParser(TParserBase):
    UrlRoot = 'https://artdrink.com.ua'

    async def Init(self):
        async with aiohttp.ClientSession() as Session:
            async with Session.get(self.UrlRoot) as Response:
                Cookie = {Val.key:Val.value for Key, Val in Response.cookies.items()}
                Cookie['language'] = 'ua'

        self.Headers = {
            '_accept': 'application/json, text/javascript',
            'cookie': self._DictToCookie(Cookie)
        }

    async def _GetData(self, aCode: str) -> dict:
        if (not self.CheckEan(aCode)):
            return

        Url = f'{self.UrlRoot}/index.php?route=module/autosearch/ajax_asr&keyword={aCode}'

        async with aiohttp.ClientSession() as Session:
            async with Session.get(Url, headers=self.Headers) as Response:
                Data = await Response.read()
                try:
                    Data = json.loads(Data)
                except ValueError:
                    Log.Print(1, 'x', f'Err: {Url}')
                    await asyncio.sleep(3)
                    return

                if (Data['pro']):
                    Product = Data['pro'][0]
                    Url = Product['href'].replace(self.UrlRoot, f'{self.UrlRoot}/ua')
                    async with Session.get(Url, headers=self.Headers) as Response:
                        Data = await Response.read()
                        ResParse = self.ParseScheme(Data)
                        Res = ResParse.get('data')
                        if (Res) and (TEan(Res['ean']).Check()):
                            Res['url'] = Url
                            return Res
