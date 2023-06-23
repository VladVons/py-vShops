# Created: 2023.05.28
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import aiohttp
from bs4 import BeautifulSoup
#
from .. import TParserBase


class TParser(TParserBase):
    CodeAllow = r'^(48)\d{11}$'
    ImageNeed = False
    UrlRoot = 'https://gepir4.gs1ua.org'

    def __init__(self):
        self.Url = f'{self.UrlRoot}/search/gtin'
        self.Headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        }
        self.Token = None

    async def Init(self):
        async with aiohttp.ClientSession() as Session:
            async with Session.get(self.Url) as Response:
                Data = await Response.read()
                Soup = BeautifulSoup(Data, 'lxml')
                Obj = Soup.find('input', attrs = {'type': 'hidden'})
                assert(Obj), 'cant find tag'
                self.Token = Obj.get('value')

                Cookie = {Val.key:Val.value for Key, Val in Response.cookies.items()}
                self.Headers['Cookie'] = self._DictToCookie(Cookie)

    async def _GetData(self, aCode: str) -> dict:
        if (not self.CheckEan(aCode)):
            return

        Payload = f'search_by_gtin%5BinterpretationResult%5D={aCode}&search_by_gtin%5BsearchType%5D=2&search_by_gtin%5B_token%5D={self.Token}'

        async with aiohttp.ClientSession() as Session:
            async with Session.post(self.Url, data=Payload, headers=self.Headers) as Response:
                Data = await Response.read()
                ResParse = self.ParseScheme(Data)
                return ResParse.get('data')
