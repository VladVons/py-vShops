# Created: 2023.02.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Sql.ADb import ListIntToComma


async def GetProductsPrice(self, aProductIds: list[int])  -> dict:
    ProductIds = ListIntToComma(aProductIds)
    return await self.ExecQuery(
        'fmtGetProductsPrice.sql',
        {'ProductIds': ProductIds}
    )

async def GetProductPriceOnDate(self, aProductId: int, aPriceId: int, aDate: str, aQty: int = 1) -> dict:
    return await self.ExecQuery(
        'fmtGetProductPriceOnDate.sql',
        {'aProductId': aProductId, 'aPriceId': aPriceId, 'aDate': aDate, 'aQty': aQty}
    )
