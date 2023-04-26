# Created: 2023.02.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


async def GetProductPriceOnDate(self, aProductId: int, aPriceId: int, aDate: str, aQty: int = 1) -> dict:
    return await self.ExecQuery(
        'fmtGet_ProductPriceOnDate.sql',
        {'aProductId': aProductId, 'aPriceId': aPriceId, 'aDate': aDate, 'aQty': aQty}
    )

async def Get_ProductPrices(self, aProductId: int) -> dict:
    return await self.ExecQuery(
        'fmtGet_ProductPrices.sql',
        {'aProductId': aProductId}
    )
