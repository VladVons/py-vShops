# Created: 2023.02.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


async def Get_PriceHist_Product(self, aProductId: int) -> dict:
    return await self.ExecQuery(
        'fmtGet_PriceHist_Product.sql',
        {'aProductId': aProductId}
    )
