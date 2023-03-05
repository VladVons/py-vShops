# Created: 2023.02.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


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
