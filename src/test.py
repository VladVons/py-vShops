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

def GetTree(aDbl: TDbList) -> dict:
    Res = {}
    for Rec in aDbl:
        ParentId = Rec.GetField('parent_id')
        Data = Res.get(ParentId, [])
        Data.append(Rec.GetField('id'))
        Res[ParentId] = Data
    return Res

async def Test_04():
    Db = TDbPg(DbAuth)
    await Db.Connect()

    DbMeta = TDbMeta(Db)
    await DbMeta.Init()
    DbModels = TDbModels('IncP/Db/Model', DbMeta)

    Dbl = TDbList().Load('Temp/TCategory.dat')
    BTree = Dbl.SearchAdd('id')
    Tree = GetTree(Dbl)
    print(Dbl)

    await Db.Close()
    print('done')

Task = Test_04()
asyncio.run(Task)
