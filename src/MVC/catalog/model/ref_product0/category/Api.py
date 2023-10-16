# Created: 2023.10.15
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Sql.ADb import ListIntToComma


async def Get_CategoriesSubCount_ParentLang(self, aLang: int, aParentIdRoot: int, aParentIds: list[int]) -> dict:
    CondParentIds = ''
    if (aParentIds):
        CondParentIds = 'and (wrpc.parent_id in (%s))' % ListIntToComma(aParentIds)

    return await self.ExecQuery(
        'fmtGet_CategoriesSubCount_ParentLang.sql',
        {'aParentIdRoot': aParentIdRoot, 'CondParentIds': CondParentIds, 'aLang': aLang}
    )

async def Get_CategoryIds_Sub(self, aCategoryIds: list[int]) -> dict:
    CategoryIds = ListIntToComma(aCategoryIds)
    return await self.ExecQuery(
        'fmtGet_CategoryIds_Sub.sql',
        {'CategoryIds': CategoryIds}
    )

async def Get_CategoriesProducts_LangImagePrice(self, aLang: str, aCategoryIds: list[int], aPriceId: int, aOrder: str, aLimit: int = 100, aOffset: int = 0) -> dict:
    CategoryIds = ListIntToComma(aCategoryIds)

    return await self.ExecQuery(
        'fmtGet_CategoriesProducts_LangImagePrice.sql',
        {'CategoryIds': CategoryIds, 'aLang': aLang, 'aPriceId': aPriceId, 'aOrder': aOrder, 'aLimit': aLimit, 'aOffset': aOffset}
    )
