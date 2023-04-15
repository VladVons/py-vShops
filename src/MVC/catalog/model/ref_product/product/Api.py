# Created: 2023.02.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
#
from Inc.Sql.ADb import ListIntToComma


async def GetProducts(self, aProductIds: list[int]) -> dict:
    ProductIds = ListIntToComma(aProductIds)
    return await self.ExecQuery(
        'fmtGetProducts.sql',
        {'aProductIds': ProductIds}
    )

async def GetProductsByIdt(self, aProductIdts: list[int]) -> dict:
    ProductIdts = ListIntToComma(aProductIdts)
    return await self.ExecQuery(
        'fmtGetProductsByIdt.sql',
        {'ProductIdts': ProductIdts}
    )

async def Get_Products_LangFilter(self, aLangId: int, aFilter: str, aLimit: int = 100, aOffset: int = 0) -> dict:
    FilterRe = [f"('%{x}%')" for x in re.split(r'\s+', aFilter)]
    return await self.ExecQuery(
        'fmtGet_Products_LangFilter.sql',
        {'aLangId': aLangId, 'aFilter': aFilter, 'FilterRe': ', '.join(FilterRe), 'aLimit': aLimit, 'aOffset': aOffset}
    )
    rp.sort_order
