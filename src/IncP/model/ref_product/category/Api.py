# Created: 2023.02.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


async def GetProductsCountInCategoriesByTenant(self, aTenantId: int) -> dict:
    return await self.ExecQuery(
        'fmtGetProductsCountInCategoriesByTenant.sql',
        {'aTenantId': aTenantId}
    )

async def GetProductsCountAndNameInCategories(self, aTenantId: int, aLangId: int) -> dict:
    '''
    get products count in all categories
    '''

    return await self.ExecQuery(
        'fmtGetProductsCountAndNameInCategories.sql',
        {'aTenantId': aTenantId, 'aLangId': aLangId}
    )

async def GetCategoriesByParent(self, aTenantId: int, aParentIdt: int = 0, aDepth: int = 99) -> dict:
    return await self.ExecQuery(
        'fmtGetCategoriesByParent.sql',
        {'aTenantId': aTenantId, 'aParentIdt': aParentIdt, 'aDepth': aDepth}
    )

async def GetCategoriesByParentWithProductCount(self, aTenantId: int, aParentIdt: int = 0) -> dict:
    return await self.ExecQuery(
        'fmtGetCategoriesByParentWithProductCount.sql',
        {'aTenantId': aTenantId, 'aParentIdt': aParentIdt}
    )
