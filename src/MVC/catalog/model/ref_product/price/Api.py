# Created: 2023.02.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Sql.ADb import ListToComma


async def Get_Price_Product(self, aProductId: int, aPriceType: list[str] = None) -> dict:
    if (not aPriceType):
        aPriceType = ['sale']

    PriceType = ListToComma(aPriceType)
    return await self.ExecQuery(
        'fmtGet_Price_Product.sql',
        {'aProductId': aProductId, 'aPriceType': PriceType}
    )

async def Get_PriceHist_Product(self, aProductId: int) -> dict:
    return await self.ExecQuery(
        'fmtGet_PriceHist_Product.sql',
        {'aProductId': aProductId}
    )

async def Get_PriceHist_ProductDate(self, aProductId: int, aPriceId: int, aDate: str, aQty: int = 1) -> dict:
    return await self.ExecQuery(
        'mtGet_Price_ProductDate.sql',
        {'aProductId': aProductId, 'aPriceId': aPriceId, 'aDate': aDate, 'aQty': aQty}
    )
