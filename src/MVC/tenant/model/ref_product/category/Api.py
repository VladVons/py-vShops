# Created: 2023.12.22
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibModel import ListIntToComma


async def Get_CategoryId_Path(self, aLangId: int, aCategoryIds: list[int]) -> dict:
    CategoryIds = ListIntToComma(aCategoryIds)
    return await self.ExecQuery(
        'fmtGet_CategoryId_Path.sql',
        {'aLangId': aLangId, 'CategoryIds': CategoryIds}
    )
