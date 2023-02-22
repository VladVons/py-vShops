import time
import json
import asyncio
#
from Inc.DbList import TDbSql, TDbList
from Inc.Sql.DbPg import TDbPg
from Inc.Sql.ADb import TDbExecPool
from Inc.Sql.DbMeta import TDbMeta
from Inc.Sql.DbModel import TDbModel
from Inc.Sql.DbModels import TDbModels
from Inc.Misc.Log import TEchoConsoleEx

from IncP.Log import Log
Log.AddEcho(TEchoConsoleEx())


DbAuth = {
    'server': 'localhost',
    'database': 'shop2',
    'user': 'admin',
    'password': '098iop'
}

def LoadJson(aFile: str) -> dict:
    with open(aFile, 'r', encoding = 'utf8') as F:
        Res = json.load(F)
    return Res

def SaveJson(aFile: str, aData, aFormat: bool = False):
    with open(aFile, 'w', encoding = 'utf-8') as F:
        if (aFormat):
            json.dump(aData, F, indent=4, sort_keys=True, ensure_ascii=False)
        else:
            json.dump(aData, F)

class TCatalogToDb():
    def __init__(self, aDbl: TDbList):
        self.Dbl = aDbl
        self.BTree = aDbl.SearchAdd('id')

    def GetTree(self) -> dict:
        Res = {}
        for Rec in self.Dbl:
            ParentId = Rec.GetField('parent_id')
            Data = Res.get(ParentId, [])
            Data.append(Rec.GetField('id'))
            Res[ParentId] = Data
        return Res

    async def SetTree(self, aTree: dict, aParentId: int):
        for x in aTree.get(aParentId, {}):
            print(aParentId, x)
            if (x in aTree):
                await self.SetTree(aTree, x)

async def Test_04():
    Db = TDbPg(DbAuth)
    await Db.Connect()

    DbMeta = TDbMeta(Db)
    await DbMeta.Init()
    DbModels = TDbModels('IncP/Model', DbMeta)

    # Dbl = TDbList().Load('Temp/TCategory.dat')
    # CatalogToDb = TCatalogToDb(Dbl)
    # Tree = CatalogToDb.GetTree()
    # await CatalogToDb.SetTree(Tree, 0)
    # print(Dbl)

    # DbModels.LoadMod('RefProduct/Category')
    # Ref = DbModels['RefProduct/Category']
    # #Sql = Ref.Sql.GetProductsCountInCategories(1, 1)
    # Sql = Ref.Sql.GetCategoriesByParent(2, 1)
    # # print(Sql)
    # Dbl = await TDbExecPool(Db.Pool).Exec(Sql)
    # print(Dbl)

    DbModels.LoadMod('RefProduct/Image')
    Ref = DbModels['RefProduct/Image']
    #Sql = Ref.Sql.GetProductsWithoutImages(1)
    Sql = Ref.Sql.GetProductsCountImages(1)
    Dbl = await TDbExecPool(Db.Pool).Exec(Sql)
    print(Dbl)

    DbModels.LoadMod('RefProduct/Lang')
    Ref = DbModels['RefProduct/Lang']
    Sql = Ref.Sql.GetProductsWithoutLang(1, 1)
    Dbl = await TDbExecPool(Db.Pool).Exec(Sql)

    DbModels.LoadMod('RefProduct/Price')
    Ref = DbModels['RefProduct/Price']
    Sql = Ref.Sql.GetProductPriceOnDate(6836, 3, '2023-02-20')
    print(Sql)
    Dbl = await TDbExecPool(Db.Pool).Exec(Sql)
    print(Dbl)
    Sql = Ref.Sql.GetProductsPrice([6836])
    Dbl = await TDbExecPool(Db.Pool).Exec(Sql)
    print(Dbl)

    await Db.Close()
    print('done')

#Task = Test_04()
#asyncio.run(Task)


import os
import sys
from Inc.Misc.FS import GetFiles
from Inc.Util.ModHelp import GetHelp

pass
