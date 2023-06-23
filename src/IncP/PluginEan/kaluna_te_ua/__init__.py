# Created: 2023.05.31
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import asyncio
import aiohttp
from bs4 import BeautifulSoup
#
from IncP.Log import Log
from .. import TParserBase


class TParser(TParserBase):
    UrlRoot = 'https://kaluna.te.ua'

    async def Init(self):
        self.Headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }

        async with aiohttp.ClientSession() as Session:
            async with Session.get(self.UrlRoot) as Response:
                Cookie = {Val.key:Val.value for Key, Val in Response.cookies.items()}
                self.Headers['Cookie'] = self._DictToCookie(Cookie)

    async def _GetData(self, aCode: str) -> dict:
        if (not self.CheckEan(aCode)):
            return

        Url = f'{self.UrlRoot}/api/search/'
        Payload = f'q={aCode}'

        async with aiohttp.ClientSession() as Session:
            async with Session.post(Url, data=Payload, headers=self.Headers) as Response:
                try:
                    Data = await Response.json()
                except ValueError:
                    Log.Print(1, 'x', f'_GetData({aCode}) Err: {Url}')
                    await asyncio.sleep(3)
                    return

                if (Data['success']):
                    #self._WriteFile('q.json', Data)
                    Soup = BeautifulSoup(Data['html'], 'lxml')
                    Obj = Soup.find('a')
                    if (Obj):
                        Url = self.UrlRoot + Obj.get('href')
                        async with Session.get(Url) as Response:
                            Data = await Response.read()
                            ResParse = self.ParseScheme(Data)
                            Res = ResParse.get('data')
                            if (Res) and (not Res['images'].endswith('no_image.jpg')):
                                Res['url'] = Url
                                return Res
