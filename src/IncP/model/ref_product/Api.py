# Created: 2023.02.22
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Sql.ADb import TDbExecPool
from . import Sql


async def AddProduct(self, aData: dict) -> dict:
    return await self.Add(aData)

async def GetProducts(self, aLangId: int, aText: str) -> dict:
    Query = Sql.GetProducts(aLangId, aText)
    Dbl = await TDbExecPool(self.DbMeta.Db.Pool).Exec(Query)
    return Dbl.Export()

async def AddHistProductSearch(self, aLangId: int, aSessionId: int, aText: str):
    Query = Sql.AddHistProductSearch(aLangId, aSessionId, aText)
    await TDbExecPool(self.DbMeta.Db.Pool).Exec(Query)
