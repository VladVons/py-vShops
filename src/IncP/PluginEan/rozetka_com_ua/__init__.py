# Created: 2023.05.29
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import aiohttp
from bs4 import BeautifulSoup
#
from Inc.Util.Obj import DeepGetByList
from .. import TParserBase


class TParser(TParserBase):
    UrlRoot = 'https://search.rozetka.com.ua'

    async def _GetData(self, aEan: str):
        async with aiohttp.ClientSession() as Session:
            Url = f'{self.UrlRoot}/ua/search/api/v6/autocomplete/?lang=ua&text={aEan}'
            async with Session.get(Url) as Response:
                Data = await Response.json()
                if (DeepGetByList(Data, ['data', 'code'], 0) == 1):
                    Products = DeepGetByList(Data, ['data', 'content', 'records', 'goods'], [])
                    if (Products):
                        Product = Products[0]
                        Code = f'({aEan})'
                        if (Code in Product['title']):
                            Url = Product['href']
                            async with Session.get(Url) as Response:
                                Data = await Response.read()
                                ResParse = self.ParseScheme(Data)
                                Res = ResParse.get('data')
                                if (Res):
                                    Res['url'] = Url
                                    Res['name'] = Product['title'].replace(Code, '').rstrip()
                                return Res
