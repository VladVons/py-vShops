# Created: 2023.05.30
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import aiohttp
from bs4 import BeautifulSoup
#
from Inc.Util.Obj import DeepGetByList
from .. import TParserBase


class TParser(TParserBase):
    UrlRoot = 'https://himopt.com.ua'

    async def _GetData(self, aCode: str) -> dict:
        if (not self.CheckEan(aCode)):
            return

        Url = f'{self.UrlRoot}/ua/search?search={aCode}'

        async with aiohttp.ClientSession() as Session:
            async with Session.get(Url) as Response:
                Data = await Response.read()
                ResParse1 = self.ParseScheme(Data, 'scheme1.json')
                Url = DeepGetByList(ResParse1, ['data', 'url'])
                if (Url):
                    async with Session.get(Url) as Response:
                        Data = await Response.read()
                        ResParse2 = self.ParseScheme(Data, 'scheme2.json')
                        Res = ResParse2.get('data')
                        if (Res):
                            Res['url'] = Url
                        return Res
