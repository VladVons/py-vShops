# Created: 2023.02.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Sql.ADb import TDbExecPool
from . import Sql


async def GetProductsLang(self, aProductId: list[int], aLangId: id) -> dict:
    Query = Sql.GetProductsLang(aProductId, aLangId)
    Dbl = await TDbExecPool(self.DbMeta.Db.Pool).Exec(Query)
    return Dbl.Export()

async def GetProductsWithoutLang(self, aTenantId: int, aLangId: int) -> dict:
    '''
    About
    '''
    Query = Sql.GetProductsWithoutLang(aTenantId, aLangId)
    Dbl = await TDbExecPool(self.DbMeta.Db.Pool).Exec(Query)
    return Dbl.Export()
