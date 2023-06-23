# Created: 2023.05.30
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import aiohttp
from bs4 import BeautifulSoup
#
from Inc.Ean import TEan
from Inc.Util.Obj import DeepGetByList
from .. import TParserBase


class TParser(TParserBase):
    UrlRoot = 'https://via.com.ua'

    async def _GetData(self, aCode: str) -> dict:
        if (not self.CheckEan(aCode)):
            return

        self.Headers = {
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'x-requested-with': 'XMLHttpRequest'
        }
        Url = f'{self.UrlRoot}/index.php?route=extension/module/uni_live_search'
        Payload = f'filter_name={aCode}'

        async with aiohttp.ClientSession() as Session:
            async with Session.post(Url, data=Payload, headers=self.Headers) as Response:
                Data = await Response.read()
                Soup = BeautifulSoup(Data, 'lxml')
                Obj = Soup.find('li', {'class': 'live-search__item'})
                if (Obj):
                    Url = Obj.get('data-href')
                    async with Session.get(Url) as Response:
                        Data = await Response.read()
                        ResParse = self.ParseScheme(Data, 'scheme2.json')
                        Res = ResParse.get('data')
                        if (Res) and (TEan(Res['ean']).Check()):
                            Res['url'] = Url
                            return Res
