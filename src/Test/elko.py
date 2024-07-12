# https://uaapi.elko.cloud/index.html

import os
import asyncio
import aiohttp


class TElko():
    def __init__(self, aToken: str):
        self.Token = aToken
        self.UrlApi = "https://uaapi.elko.cloud/v3.0"

    async def Request(self, aPath: str) -> dict:
        Headers = {
            'Authorization': f'Bearer {self.Token}',
            'cache-control': 'no-cache'
        }

        async with aiohttp.ClientSession() as Session:
            async with Session.get(f'{self.UrlApi}/{aPath}', headers=Headers) as Response:
                if (Response.status == 200):
                    Res = await Response.json()
                else:
                    Res = {'err': Response.reason}
                return Res

    async def GetCategories(self):
        return await self.Request('Catalogs/CategoryList')

    async def GetCategoryProducts(self, aCategoryId: str) -> dict:
        return await self.Request(f'Catalogs/Products?elkoCode={aCategoryId}&lang=UA&showOnlyAvaliable')

    async def GetProductDescr(self, aProductId: str) -> dict:
        return await self.Request(f'Catalogs/Products/{aProductId}/Description?lang=UA')

    async def GetProductMedia(self, aProductId: str) -> dict:
        return await self.Request(f'Catalogs/MediaItems/{aProductId}')


async def Main():
    Token = os.getenv('ELKO_TOKEN')
    Elko = TElko(Token)

    #Data = await Elko.GetCategories()
    #for x in Data:
    #    print(x['translation']['ua'], x['code'])

    #ElkoCode = "TSL"
    #Data = await Elko.GetCategoryProducts(ElkoCode)
    #print(Data)

    ProductId = '1419230'
    Data = await Elko.GetProductDescr(ProductId)
    print(Data)

    Data = await Elko.GetProductMedia(ProductId)
    print(Data)



asyncio.run(Main())
