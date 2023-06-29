# Created: 2023.02.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


async def Get_PriceHist_Product(self, aProductId: int) -> dict:
    return await self.ExecQuery(
        'fmtGet_PriceHist_Product.sql',
        {'aProductId': aProductId}
    )

async def Get_Price_ProductDate(self, aProductId: int, aPriceId: int, aDate: str, aQty: int = 1) -> dict:
    return await self.ExecQuery(
        'mtGet_Price_ProductDate.sql',
        {'aProductId': aProductId, 'aPriceId': aPriceId, 'aDate': aDate, 'aQty': aQty}
    )
