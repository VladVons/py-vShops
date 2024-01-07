# Created: 2023.12.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibModel import ListIntToComma


async def Get_ProductsInf_Ids(self, aLangId: int, aIds: list[int]) -> dict:
    Ids = ListIntToComma(aIds)

    return await self.ExecQuery(
        'fmtGet_ProductsInf_Ids.sql',
        {'aLangId': aLangId, 'Ids': Ids}
    )

async def Get_ProductInf_Id(self, aLangId: int, aId: int) -> dict:
    return await self.ExecQuery(
        'fmtGet_ProductInf_Id.sql',
        {'aLangId': aLangId, 'aId': aId}
    )

async def Get_Product_Images(self, aProductId: int) -> dict:
    return await self.ExecQuery(
        'fmtGet_Product_Images.sql',
        {'aProductId': aProductId}
    )
