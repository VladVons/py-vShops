# Created: 2023.02.22
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Sql.ADb import TDbExecPool
from . import Sql


async def AddProduct(self, aData: dict) -> dict:
    return await self.Add(aData)

async def GetProducts(self, aLangId: int, aTitle: str) -> dict:
    Query = Sql.GetProducts(aLangId, aTitle)
    Dbl = await TDbExecPool(self.DbMeta.Db.Pool).Exec(Query)
    return Dbl.Export()
