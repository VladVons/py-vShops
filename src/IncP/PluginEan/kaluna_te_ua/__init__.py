import re
import aiohttp
from bs4 import BeautifulSoup
#
from .. import TParserBase


class TParser(TParserBase):
    UrlRoot = 'https://kaluna.te.ua'

    async def _Init(self):
        self.Headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }

        async with aiohttp.ClientSession() as Session:
            async with Session.get(self.UrlRoot) as Response:
                Arr = [f'{Val.key}={Val.value}' for Key, Val in Response.cookies.items()]
                self.Headers['Cookie'] = '; '.join(Arr)

    async def _GetData(self, aEan: str):
        Url = f'{self.UrlRoot}/api/search/'
        Payload = f'q={aEan}'

        async with aiohttp.ClientSession() as Session:
            async with Session.post(Url, data=Payload, headers=self.Headers) as Response:
                Data = await Response.json()
                if (Data['success']):
                    Soup = BeautifulSoup(Data['html'], 'lxml')
                    Url = self.UrlRoot + Soup.find('a').get('href')
                    async with Session.get(Url) as Response:
                        Data = await Response.read()
                        ResParse = self.ParseScheme(Data)
                        Res = ResParse.get('data')
                        if (Res):
                            Res['url'] = Url
                            return Res
