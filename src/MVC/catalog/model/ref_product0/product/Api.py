# Created: 2023.02.16
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
from IncP.LibModel import ListIntToComma


async def Get_ProductsRnd_LangImagePrice(self, aLangId: int, aLimit: int = 24) -> dict:
    return await self.ExecQuery(
        'fmtGet_ProductsRnd_LangImagePrice.sql',
        {'aLangId': aLangId, 'aLimit': aLimit}
    )

async def Get_ProductsLastView_LangImagePrice(self, aLangId: int, aSessionId: int, aLimit: int = 6) -> dict:
    return await self.ExecQuery(
        'fmtGet_ProductsLastView_LangImagePrice.sql',
        {'aLangId': aLangId, 'aSessionId': aSessionId, 'aLimit': aLimit}
    )

async def Get_Product_LangId(self, aLangId: int, aProductId: int) -> dict:
    return await self.ExecQuery(
        'fmtGet_Product_LangId.sql',
        {'aLangId': aLangId, 'aProductId': aProductId}
    )

async def Get_Products_LangFilter(self, aLangId: int, aFilter: str, aOrder: str, aLimit: int = 100, aOffset: int = 0) -> dict:
    FilterRe = [f"('%{x}%')" for x in re.split(r'\s+', aFilter)]
    return await self.ExecQuery(
        'fmtGet_Products_LangFilter.sql',
        {'aLangId': aLangId, 'aFilter': aFilter, 'FilterRe': ', '.join(FilterRe), 'aOrder': aOrder, 'aLimit': aLimit, 'aOffset': aOffset}
    )

async def Get_Products_LangAjax(self, aLangId: int, aFilter: str) -> dict:
    FilterRe = [f"('%{x}%')" for x in re.split(r'\s+', aFilter)]
    return await self.ExecQuery(
        'fmtGet_Products_LangAjax.sql',
        {'aLangId': aLangId, 'FilterRe': ', '.join(FilterRe)}
    )

async def Get_ProductsAttr(self, aLangId: int, aProductIds: list[int]) -> dict:
    ProductIds = ListIntToComma(aProductIds)
    return await self.ExecQuery(
        'fmtGet_ProductsAttr.sql',
        {'aLangId': aLangId, 'ProductIds': ProductIds}
    )
