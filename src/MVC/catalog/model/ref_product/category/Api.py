# Created: 2023.02.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Sql.ADb import ListIntToComma


async def Get_ProductsCount_Tenant(self, aTenantId: int) -> dict:
    return await self.ExecQuery(
        'fmtGet_ProductsCount_Tenant.sql',
        {'aTenantId': aTenantId}
    )

async def Get_ProductsCount_TenantParent(self, aTenantId: int, aParentIdt: int = 0) -> dict:
    return await self.ExecQuery(
        'fmtGet_ProductsCount_TenantParent.sql',
        {'aTenantId': aTenantId, 'aParentIdt': aParentIdt}
    )

async def Get_CategoriesProductsCountName_TenantLang(self, aTenantId: int, aLangId: int) -> dict:
    '''
    get products count in all categories
    '''

    return await self.ExecQuery(
        'fmtGet_CategoriesProductsCountName_TenantLang.sql',
        {'aTenantId': aTenantId, 'aLangId': aLangId}
    )

async def Get_Categories_TenantParent(self, aTenantId: int, aParentIdt: int, aDepth: int = 99) -> dict:
    return await self.ExecQuery(
        'fmtGet_Categories_TenantParent.sql',
        {'aTenantId': aTenantId, 'aParentIdt': aParentIdt, 'aDepth': aDepth}
    )

async def Get_Categories_TenantParentLang(self, aTenantId: int, aParentIdts: list[int], aLangId: int, aDepth: int = 99) -> dict:
    ParentIdts = ListIntToComma(aParentIdts)
    return await self.ExecQuery(
        'fmtGet_Categories_TenantParentLang.sql',
        {'aTenantId': aTenantId, 'aParentIdts': ParentIdts, 'aLangId': aLangId, 'aDepth': aDepth}
    )

async def Get_CategoriesSubCount_TenantParentLang(self, aTenantId: int, aParentIdtRoot: int, aParentIdts: list[int], aLangId: int) -> dict:
    CondParentIdts = ''
    if (aParentIdts):
        CondParentIdts = 'and (wrpc.parent_idt in (%s))' % ListIntToComma(aParentIdts)

    return await self.ExecQuery(
        'fmtGet_CategoriesSubCount_TenantParentLang.sql',
        {'aTenantId': aTenantId, 'aParentIdtRoot': aParentIdtRoot, 'CondParentIdts': CondParentIdts, 'aLangId': aLangId}
    )
