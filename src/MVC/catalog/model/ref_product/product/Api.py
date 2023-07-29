# Created: 2023.02.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re


async def Get_Products_LangFilter(self, aLangId: int, aFilter: str, aOrder: str, aLimit: int = 100, aOffset: int = 0) -> dict:
    FilterRe = [f"('%{x}%')" for x in re.split(r'\s+', aFilter)]
    return await self.ExecQuery(
        'fmtGet_Products_LangFilter.sql',
        {'aLangId': aLangId, 'aFilter': aFilter, 'FilterRe': ', '.join(FilterRe), 'aOrder': aOrder, 'aLimit': aLimit, 'aOffset': aOffset}
    )

async def Get_Products0_LangFilter(self, aLang: str, aFilter: str, aOrder: str, aLimit: int = 100, aOffset: int = 0) -> dict:
    FilterRe = [f"('%{x}%')" for x in re.split(r'\s+', aFilter)]
    return await self.ExecQuery(
        'fmtGet_Products0_LangFilter.sql',
        {'aLang': aLang, 'aFilter': aFilter, 'FilterRe': ', '.join(FilterRe), 'aOrder': aOrder, 'aLimit': aLimit, 'aOffset': aOffset}
    )

async def Get_Product_LangId(self, aLangId: int, aProductId: int) -> dict:
    return await self.ExecQuery(
        'fmtGet_Product_LangId.sql',
        {'aLangId': aLangId, 'aProductId': aProductId}
    )

async def Get_Product0_LangId(self, aLang: str, aProductId: int) -> dict:
    return await self.ExecQuery(
        'fmtGet_Product0_LangId.sql',
        {'aLang': aLang, 'aProductId': aProductId}
    )
