# Created: 2023.10.15
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibModel import ListIntToComma, ListToComma


async def Get_CategoriesSubCount_ParentLang(self, aLangId: int, aParentIdRoot: int, aParentIds: list[int] = None) -> dict:
    CondParentIds = ''
    if (aParentIds):
        CondParentIds = 'and (wrpc.parent_id in (%s))' % ListIntToComma(aParentIds)

    return await self.ExecQuery(
        'fmtGet_CategoriesSubCount_ParentLang.sql',
        {'aParentIdRoot': aParentIdRoot, 'CondParentIds': CondParentIds, 'aLangId': aLangId}
    )

async def Get_CategoryIds_Sub(self, aCategoryIds: list[int]) -> dict:
    CategoryIds = ListIntToComma(aCategoryIds)
    return await self.ExecQuery(
        'fmtGet_CategoryIds_Sub.sql',
        {'CategoryIds': CategoryIds}
    )

async def Get_CategoriesProducts_LangImagePrice(self, aLangId: int, aCategoryIds: list[int], aPriceId: int, aOrder: str, aLimit: int = 100, aOffset: int = 0) -> dict:
    CategoryIds = ListIntToComma(aCategoryIds)

    return await self.ExecQuery(
        'fmtGet_CategoriesProducts_LangImagePrice.sql',
        {'CategoryIds': CategoryIds, 'aLangId': aLangId, 'aPriceId': aPriceId, 'aOrder': aOrder, 'aLimit': aLimit, 'aOffset': aOffset}
    )

async def Get_CategoryId_Path(self, aLangId: int, aCategoryIds: list[int]) -> dict:
    CategoryIds = ListIntToComma(aCategoryIds)
    return await self.ExecQuery(
        'fmtGet_CategoryId_Path.sql',
        {'aLangId': aLangId, 'CategoryIds': CategoryIds}
    )

async def Get_Category_LangId(self, aLangId: int, aCategoryId: int) -> dict:
    return await self.ExecQuery(
        'fmtGet_Category_LangId.sql',
        {'aLangId': aLangId, 'aCategoryId': aCategoryId}
    )

async def Get_CategoryAttr(self, aLangId: int, aCategoryId: int) -> dict:
    return await self.ExecQuery(
        'fmtGet_CategoryAttr.sql',
        {'aLangId': aLangId, 'aCategoryId': aCategoryId}
    )

async def Get_CategoryAttrFilter(self, aLangId: int, aCategoryId: int, aAttr: dict) -> dict:
    Arr = []
    for AttrId, AttrVal in aAttr.items():
        Values = ListToComma(AttrVal)
        Arr.append(f"(rpa.attr_id = {AttrId} and rpa.val in ({Values}))")
    CondAttrAndVal_ORs = ' or\n'.join(Arr)

    return await self.ExecQuery(
        'fmtGet_CategoryAttrFilter.sql',
        {
            'aLangId': aLangId,
            'aCategoryId': aCategoryId,
            'CondAttrAndVal_ORs': CondAttrAndVal_ORs,
            'NumberOf_ORs': len(aAttr)
        }
    )
