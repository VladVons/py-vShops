# Created: 2023.12.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re


async def Get_Product_LangId(self, aLangId: int, aTenantId: int, aProductId: int) -> dict:
    return await self.ExecQuery(
        'fmtGet_Product_LangId.sql',
        {'aLangId': aLangId, 'aTenantId': aTenantId, 'aProductId': aProductId}
    )

async def Get_Products_LangFilter(self, aLangId: int, aTenantId: int, aFilter: str, aOrder: str, aLimit: int = 100, aOffset: int = 0) -> dict:
    FilterRe = [f"('%{x}%')" for x in re.split(r'\s+', aFilter)]
    return await self.ExecQuery(
        'fmtGet_Products_LangFilter.sql',
        {'aLangId': aLangId, 'aTenantId': aTenantId, 'aFilter': aFilter, 'FilterRe': ', '.join(FilterRe), 'aOrder': aOrder, 'aLimit': aLimit, 'aOffset': aOffset}
    )

async def Get_ProductsStat(self, aTenantId: int) -> dict:
    return await self.ExecQuery(
        'fmtGet_ProductsStat.sql',
        {'aTenantId': aTenantId}
    )
