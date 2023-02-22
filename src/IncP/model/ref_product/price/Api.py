# Created: 2023.02.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Sql.ADb import TDbExecPool
from . import Sql


async def GetProductsPrice(self, aProductId: list[int])  -> dict:
    Query = Sql.GetProductsPrice(aProductId) 
    Dbl = await TDbExecPool(self.DbMeta.Db.Pool).Exec(Query)
    return Dbl.Export()

async def GetProductPriceOnDate(self, aProductId: int, aPriceId: int, aDate: str, aQty: int = 1) -> dict:
    Query = Sql.GetProductPriceOnDate(aProductId, aPriceId, aDate, aQty)
    Dbl = await TDbExecPool(self.DbMeta.Db.Pool).Exec(Query)
    return Dbl.Export()
