import time
import json
import asyncio
#
from Inc.Db.DbList import TDbSql, TDbListSafe, TDbList
from Inc.UtilP.Db.DbPg import TDbPg
from Inc.UtilP.Log import TEchoConsoleEx
from Inc.UtilP.Db.DbMeta import TDbMeta
from Inc.UtilP.Db.DbModels import TDbModels
#
from Inc.UtilP.Db.DbModel import TDbModel

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
    DbModels = TDbModels('IncP/Db/Model', DbMeta)

    Dbl = TDbList().Load('Temp/TCategory.dat')
    CatalogToDb = TCatalogToDb(Dbl)
    Tree = CatalogToDb.GetTree()
    await CatalogToDb.SetTree(Tree, 0)
    print(Dbl)

    await Db.Close()
    print('done')

Task = Test_04()
asyncio.run(Task)
