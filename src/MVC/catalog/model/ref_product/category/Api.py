# # Created: 2023.02.21
# # Author: Vladimir Vons <VladVons@gmail.com>
# # License: GNU, see LICENSE for more details


from Inc.Sql.ADb import ListIntToComma


async def Get_CategoriesSubCount_TenantParentLang(self, aTenantId: int, aParentIdtRoot: int, aParentIdts: list[int], aLangId: int) -> dict:
    CondParentIdts = ''
    if (aParentIdts):
        CondParentIdts = 'and (wrpc.parent_idt in (%s))' % ListIntToComma(aParentIdts)

    return await self.ExecQuery(
        'fmtGet_CategoriesSubCount_TenantParentLang.sql',
        {'aTenantId': aTenantId, 'aParentIdtRoot': aParentIdtRoot, 'CondParentIdts': CondParentIdts, 'aLangId': aLangId}
    )

async def Get_Categories_TenantParentLang(self, aTenantId: int, aParentIdtRoot: int, aParentIdts: list[int], aLangId: int, aDepth: int = 99) -> dict:
    CondParentIdts = ''
    if (aParentIdts):
        CondParentIdts = 'and (parent_idt in (%s))' % ListIntToComma(aParentIdts)

    return await self.ExecQuery(
        'fmtGet_Categories_TenantParentLang.sql',
        {'aTenantId': aTenantId, 'aParentIdtRoot': aParentIdtRoot, 'CondParentIdts': CondParentIdts, 'aLangId': aLangId}
    )

async def Get_CategoriesProducts_LangImagePrice(self, aCategoryIds: list[int], aLangId: int, aPriceId: int, aOrder: str, aLimit: int = 100, aOffset: int = 0) -> dict:
    CategoryIds = ListIntToComma(aCategoryIds)

    return await self.ExecQuery(
        'fmtGet_CategoriesProducts_LangImagePrice.sql',
        {'CategoryIds': CategoryIds, 'aLangId': aLangId, 'aPriceId': aPriceId, 'aOrder': aOrder, 'aLimit': aLimit, 'aOffset': aOffset}
    )

async def Get_CategoryPath_Lang(self, aLangId: int, aIds: list[int]) -> dict:
    Ids = ListIntToComma(aIds)
    return await self.ExecQuery(
        'fmtGet_CategoryPath_Lang.sql',
        {'aLangId': aLangId, 'Ids': Ids}
    )
