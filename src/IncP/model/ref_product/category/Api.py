# Created: 2023.02.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Sql.ADb import TDbExecPool
from . import Sql


async def GetProductsCountAndNameInCategories(self, aTenantId: int, aLangId: int) -> dict:
    '''
    get products count in all categories
    '''

    Query = Sql.GetProductsCountAndNameInCategories(aTenantId, aLangId)
    Dbl = await TDbExecPool(self.DbMeta.Db.Pool).Exec(Query)
    return Dbl.Export()

async def GetCategoriesByParent(self, aTenantId: int, aParentId: int = 0, aDepth: int = 99) -> dict:
    Query = self.GetQuery(
        'fmtGetCategoriesByParent.sql',
        {'aTenantId': aTenantId, 'aParentIdt': aParentId, 'aDepth': aDepth}
    )
    Dbl = await TDbExecPool(self.DbMeta.Db.Pool).Exec(Query)
    return Dbl.Export()

async def GetCategoriesByParentWithProductCount(self, aTenantId: int, aParentId: int = 0) -> dict:
    Query = Sql.GetCategoriesByParentWithProductCount(aTenantId, aParentId)
    Dbl = await TDbExecPool(self.DbMeta.Db.Pool).Exec(Query)
    return Dbl.Export()
