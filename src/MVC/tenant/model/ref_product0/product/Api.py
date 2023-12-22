# Created: 2023.12.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibModel import ListIntToComma


async def ProductsInf_Ids(self, aLangId: int, aIds: list[int]) -> dict:
    Ids = ListIntToComma(aIds)

    return await self.ExecQuery(
        'fmtGet_ProductsInf_Ids.sql',
        {'aLangId': aLangId, 'Ids': Ids}
    )
