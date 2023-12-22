# Created: 2023.12.22
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibModel import ListIntToComma


async def Get_CategoryId_Path(self, aLangId: int, aTenantId: int, aCategoryIds: list[int]) -> dict:
    CategoryIds = ListIntToComma(aCategoryIds)
    return await self.ExecQuery(
        'fmtGet_CategoryId_Path.sql',
        {'aLangId': aLangId, 'aTenantId': aTenantId, 'CategoryIds': CategoryIds}
    )

async def Get_CategoryIdt_Path(self, aLangId: int, aTenantId: int, aCategoryIdts: list[int]) -> dict:
    CategoryIdts = ListIntToComma(aCategoryIdts)
    return await self.ExecQuery(
        'fmtGet_CategoryIdt_Path.sql',
        {'aLangId': aLangId, 'aTenantId': aTenantId, 'CategoryIdts': CategoryIdts}
    )
