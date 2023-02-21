# Created: 2023.02.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Sql.ADb import TDbExecPool
from . import Sql


async def GetProductsImages(self, aProductId: list[int]) -> dict:
    Query = Sql.GetProductsImages(aProductId)
    Dbl = await TDbExecPool(self.DbMeta.Db.Pool).Exec(Query)
    return Dbl.Export()

async def GetProductImages(self, aProductId: int) -> dict:
    Query = Sql.GetProductImages(aProductId)
    Dbl = await TDbExecPool(self.DbMeta.Db.Pool).Exec(Query)
    return Dbl.Export()

async def GetProductsWithoutImages(self, aTenantId: int) -> dict:
    Query = Sql.GetProductsWithoutImages(aTenantId)
    Dbl = await TDbExecPool(self.DbMeta.Db.Pool).Exec(Query)
    return Dbl.Export()

async def GetProductsCountImages(self, aTenantId: int) -> dict:
    Query = Sql.GetProductsCountImages(aTenantId)
    Dbl = await TDbExecPool(self.DbMeta.Db.Pool).Exec(Query)
    return Dbl.Export()
