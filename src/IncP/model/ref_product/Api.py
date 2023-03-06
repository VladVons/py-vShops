# Created: 2023.02.22
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re


async def AddProduct(self, aData: dict) -> dict:
    return await self.Add(aData)

async def GetProducts(self, aLangId: int, aText: str) -> dict:
    Title = [f"('%{x}%')" for x in re.split(r'\s+', aText)]
    Title = ', '.join(Title)

    return await self.ExecQuery(
        'fmtGetProducts.sql',
        {'aLangId': aLangId, 'Title': Title}
    )

async def AddHistProductSearch(self, aLangId: int, aSessionId: int, aText: str):
    await self.ExecQuery(
        'fmtAddHistProductSearch.sql',
        {'aLangId': aLangId, 'aSessionId': aSessionId, 'aText': aText}
    )
