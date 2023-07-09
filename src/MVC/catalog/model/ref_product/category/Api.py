# # Created: 2023.02.21
# # Author: Vladimir Vons <VladVons@gmail.com>
# # License: GNU, see LICENSE for more details


from Inc.Sql.ADb import ListIntToComma


async def Get_CategoriesSubCount_TenantParentLang(self, aLangId: int, aTenantId: int, aParentIdtRoot: int, aParentIdts: list[int]) -> dict:
    CondParentIdts = ''
    if (aParentIdts):
        CondParentIdts = 'and (wrpc.parent_idt in (%s))' % ListIntToComma(aParentIdts)

    return await self.ExecQuery(
        'fmtGet_CategoriesSubCount_TenantParentLang.sql',
        {'aTenantId': aTenantId, 'aParentIdtRoot': aParentIdtRoot, 'CondParentIdts': CondParentIdts, 'aLangId': aLangId}
    )

async def Get_Categories_TenantParentLang(self, aLangId: int, aTenantId: int, aParentIdtRoot: int, aParentIdts: list[int]) -> dict:
    CondParentIdts = ''
    if (aParentIdts):
        CondParentIdts = 'and (parent_idt in (%s))' % ListIntToComma(aParentIdts)

    return await self.ExecQuery(
        'fmtGet_Categories_TenantParentLang.sql',
        {'aTenantId': aTenantId, 'aParentIdtRoot': aParentIdtRoot, 'CondParentIdts': CondParentIdts, 'aLangId': aLangId}
    )

async def Get_CategoriesProducts_LangImagePrice(self, aLangId: int, aCategoryIds: list[int], aPriceId: int, aOrder: str, aLimit: int = 100, aOffset: int = 0) -> dict:
    CategoryIds = ListIntToComma(aCategoryIds)

    return await self.ExecQuery(
        'fmtGet_CategoriesProducts_LangImagePrice.sql',
        {'CategoryIds': CategoryIds, 'aLangId': aLangId, 'aPriceId': aPriceId, 'aOrder': aOrder, 'aLimit': aLimit, 'aOffset': aOffset}
    )

async def Get_CategoriesProducts0_LangImagePrice(self, aLangId: int, aCategoryIds: list[int], aPriceId: int, aOrder: str, aLimit: int = 100, aOffset: int = 0) -> dict:
    CategoryIds = ListIntToComma(aCategoryIds)

    return await self.ExecQuery(
        'fmtGet_CategoriesProducts0_LangImagePrice.sql',
        {'CategoryIds': CategoryIds, 'aLangId': aLangId, 'aPriceId': aPriceId, 'aOrder': aOrder, 'aLimit': aLimit, 'aOffset': aOffset}
    )

async def Get_CategoryId_Path(self, aLangId: int, aCategoryIds: list[int]) -> dict:
    CategoryIds = ListIntToComma(aCategoryIds)
    return await self.ExecQuery(
        'fmtGet_CategoryId_Path.sql',
        {'aLangId': aLangId, 'CategoryIds': CategoryIds}
    )

async def Get_CategoryIdt_Path(self, aLangId: int, aCategoryIdts: list[int], aTenantId: int) -> dict:
    CategoryIdts = ListIntToComma(aCategoryIdts)
    return await self.ExecQuery(
        'fmtGet_CategoryIdt_Path.sql',
        {'aLangId': aLangId, 'CategoryIdts': CategoryIdts, 'aTenantId': aTenantId}
    )

async def Get_CategoryIdtTenant_Sub(self, aCategoryIdt: int, aTenantId: int) -> dict:
    return await self.ExecQuery(
        'fmtGet_CategoryIdtTenant_Sub.sql',
        {'aCategoryIdt': aCategoryIdt, 'aTenantId': aTenantId}
    )
