# # Created: 2023.02.21
# # Author: Vladimir Vons <VladVons@gmail.com>
# # License: GNU, see LICENSE for more details


from Inc.Sql.ADb import ListIntToComma


async def Get_CategoriesSubCount_TenantParentLang(self, aLang: int, aTenantId: int, aParentIdtRoot: int, aParentIdts: list[int]) -> dict:
    CondParentIdts = ''
    if (aParentIdts):
        CondParentIdts = 'and (wrpc.parent_idt in (%s))' % ListIntToComma(aParentIdts)

    return await self.ExecQuery(
        'fmtGet_CategoriesSubCount_TenantParentLang.sql',
        {'aTenantId': aTenantId, 'aParentIdtRoot': aParentIdtRoot, 'CondParentIdts': CondParentIdts, 'aLang': aLang}
    )

async def Get_Categories_TenantParentLang(self, aLang: str, aTenantId: int, aParentIdtRoot: int, aParentIdts: list[int]) -> dict:
    CondParentIdts = ''
    if (aParentIdts):
        CondParentIdts = 'and (parent_idt in (%s))' % ListIntToComma(aParentIdts)

    return await self.ExecQuery(
        'fmtGet_Categories_TenantParentLang.sql',
        {'aTenantId': aTenantId, 'aParentIdtRoot': aParentIdtRoot, 'CondParentIdts': CondParentIdts, 'aLang': aLang}
    )

async def Get_CategoriesProducts_LangImagePrice(self, aLangId: int, aCategoryIds: list[int], aPriceId: int, aOrder: str, aLimit: int = 100, aOffset: int = 0) -> dict:
    CategoryIds = ListIntToComma(aCategoryIds)

    return await self.ExecQuery(
        'fmtGet_CategoriesProducts_LangImagePrice.sql',
        {'CategoryIds': CategoryIds, 'aLangId': aLangId, 'aPriceId': aPriceId, 'aOrder': aOrder, 'aLimit': aLimit, 'aOffset': aOffset}
    )

async def Get_CategoriesProducts0_LangImagePrice(self, aLang: str, aCategoryIds: list[int], aPriceId: int, aOrder: str, aLimit: int = 100, aOffset: int = 0) -> dict:
    CategoryIds = ListIntToComma(aCategoryIds)

    return await self.ExecQuery(
        'fmtGet_CategoriesProducts0_LangImagePrice.sql',
        {'CategoryIds': CategoryIds, 'aLang': aLang, 'aPriceId': aPriceId, 'aOrder': aOrder, 'aLimit': aLimit, 'aOffset': aOffset}
    )

async def Get_CategoryId_Path(self, aLang: str, aCategoryIds: list[int]) -> dict:
    CategoryIds = ListIntToComma(aCategoryIds)
    return await self.ExecQuery(
        'fmtGet_CategoryId_Path.sql',
        {'aLang': aLang, 'CategoryIds': CategoryIds}
    )

async def Get_CategoryIdt_Path(self, aLang: str, aCategoryIdts: list[int], aTenantId: int) -> dict:
    CategoryIdts = ListIntToComma(aCategoryIdts)
    return await self.ExecQuery(
        'fmtGet_CategoryIdt_Path.sql',
        {'aLang': aLang, 'CategoryIdts': CategoryIdts, 'aTenantId': aTenantId}
    )

async def Get_CategoryIdtsTenant_Sub(self, aCategoryIdts: list[int], aTenantId: int) -> dict:
    CategoryIdts = ListIntToComma(aCategoryIdts)
    return await self.ExecQuery(
        'fmtGet_CategoryIdtsTenant_Sub.sql',
        {'CategoryIdts': CategoryIdts, 'aTenantId': aTenantId}
    )

async def Get_ProductIds_PathIdt(self, aProductIds: list[int]) -> dict:
    ProductIds = ListIntToComma(aProductIds)
    return await self.ExecQuery(
        'fmtGet_ProductIds_PathIdt.sql',
        {'ProductIds': ProductIds}
    )

