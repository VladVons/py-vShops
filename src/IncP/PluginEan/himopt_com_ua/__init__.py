import aiohttp
from bs4 import BeautifulSoup
#
from Inc.Util.Obj import DeepGetByList
from .. import TParserBase


class TParser(TParserBase):
    UrlRoot = 'https://himopt.com.ua'

    async def _GetData(self, aEan: str):
        async with aiohttp.ClientSession() as Session:
            Url = f'{self.UrlRoot}/ua/search?search={aEan}'
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
