# Created: 2023.06.02
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
import aiohttp
from bs4 import BeautifulSoup
#
from Inc.Ean import TEan
from Inc.Util.Obj import DeepGetByList
from .. import TParserBase


class TParser(TParserBase):
    UrlRoot = 'https://artdrink.com.ua'

    async def _Init(self):
        async with aiohttp.ClientSession() as Session:
            async with Session.get(self.UrlRoot) as Response:
                Cookie = {Val.key:Val.value for Key, Val in Response.cookies.items()}
                Cookie['language'] = 'ua'

        self.Headers = {
            'accept': 'application/json, text/javascript',
            'cookie': self._DictToCookie(Cookie)
        }

    async def _GetData(self, aEan: str):
        Url = f'{self.UrlRoot}/index.php?route=module/autosearch/ajax_asr&keyword={aEan}'
        async with aiohttp.ClientSession() as Session:
            async with Session.get(Url, headers=self.Headers) as Response:
                Data = await Response.read()
                Data = json.loads(Data)
                if (Data['pro']):
                    Product = Data['pro'][0]
                    Url = Product['href']
                    async with Session.get(Url) as Response:
                        Data = await Response.read()
                        ResParse = self.ParseScheme(Data, 'scheme2.json')
                        Res = ResParse.get('data')
                        if (Res) and (TEan(Res['ean']).Check()):
                            Res['url'] = Url
                            return Res
