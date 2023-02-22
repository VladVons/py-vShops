# Created: 2023.02.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Sql.ADb import TDbExecPool
from . import Sql


async def GetProducts(self, aProductId: list[int]) -> dict:
    Query = Sql.GetProducts(aProductId)
    Dbl = await TDbExecPool(self.DbMeta.Db.Pool).Exec(Query)
    return Dbl.Export()

async def GetProductsByIdt(self, aProductId: list[int]) -> dict:
    Query = Sql.GetProductsByIdt(aProductId)
    Dbl = await TDbExecPool(self.DbMeta.Db.Pool).Exec(Query)
    return Dbl.Export()
