# Created: 2023.05.29
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import aiohttp
from bs4 import BeautifulSoup
#
from Inc.Ean import TEan
from .. import TParserBase


class TParser(TParserBase):
    UrlRoot = 'https://fozzyshop.ua'

    async def _GetData(self, aCode: str) -> dict:
        if (not self.CheckEan(aCode)):
            return

        Headers = {
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'accept': 'application/json'
        }
        Url = f'{self.UrlRoot}/search'
        Payload = f's={aCode}&resultsPerPage=1&ajax=true'

        async with aiohttp.ClientSession() as Session:
            async with Session.post(Url, data=Payload, headers=Headers) as Response:
                Data = await Response.json()
                if (Data['products']):
                    Product = Data['products'][0]
                    Url = Product['url']
                    # Name = Product['name']
                    # Image = DeepGetByList(Product, ["cover", "bySize", "thickbox_default", "url"])
                    async with Session.get(Url) as Response:
                        Data = await Response.read()
                        ResParse = self.ParseScheme(Data)
                        Res = ResParse.get('data')
                        if (Res) and (TEan(Res['ean']).Check()):
                            Res['url'] = Url
                            return Res
