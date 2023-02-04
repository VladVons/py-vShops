import time
import json
import asyncio
#
from Inc.Db.DbList import TDbSql
from Inc.UtilP.Db.ADb import ListToComma
from Inc.UtilP.Db.DbPg import TDbPg
from Inc.UtilP.Log import TEchoConsoleEx
from Inc.UtilP.Db.DbMeta import TDbMeta
from Inc.UtilP.Db.DbModels import TDbModels
#
from Inc.UtilP.Db.DbModel import TDbModel


from IncP.Log import Log
Log.AddEcho(TEchoConsoleEx())


DbAuth = {
    'Server': 'localhost',
    'Database': 'shop2',
    'User': 'admin',
    'Password': '098iop'
}

def LoadJson(aPath: str) -> dict:
    with open(aPath, 'r', encoding = 'utf8') as F:
        Res = json.load(F)
    return Res

def Test_01():
    Data = LoadJson('Temp/ProductDbl-1.json')
    Dbl = TDbSql()
    for x in Data:
        Dbl.Import(x, False)
        print(Dbl)

async def Test_02():
    Db = TDbPg(DbAuth)
    await Db.Connect()

    #q1 = await Db.Exec("insert into ref_lang (title) values ('test')")
    #q2 = await Db.Exec("select * from ref_lang")

    DbMeta = TDbMeta(Db)
    await DbMeta.Init()
    DbModels = TDbModels('IncP/Db/Model', DbMeta)

    # Data = LoadJson('Temp/Product0.json')
    # DbModels.LoadMod('RefProduct0')
    # Ref = DbModels['RefProduct0']
    # Res1 = await Ref.Add(Data)
    # print(Res1)
    # #Res1 = await Ref.Del(199)
    # #print(Res1)

    # Data = LoadJson('Temp/Product0A.json')
    # DbModels.LoadMod('RefProduct0')
    # Ref = DbModels['RefProduct0']
    # Res1 = await Ref.AddList(Data)
    # print(Res1)
    # #Res1 = await Ref.Del(199)
    # #print(Res1)

    # Data = LoadJson('Temp/Product0Category.json')
    # DbModels.LoadMod('RefProduct0Category')
    # Ref = DbModels['RefProduct0Category']
    # Res1 = await Ref.Add(Data)
    # print(Res1)

    # Data = LoadJson('Temp/Product0CategoryA.json')
    # DbModels.LoadMod('RefProduct0Category')
    # Ref = DbModels['RefProduct0Category']
    # Res1 = await Ref.AddList(Data)
    # print(Res1)

    Data = LoadJson('Temp/Product.json')
    DbModels.LoadMod('RefProduct')
    Ref = DbModels['RefProduct']
    Res1 = await Ref.Add(Data)
    print(Res1)
    # #Res1 = await Ref.Del(14)
    # #print(Res1)

    # Data = LoadJson('Temp/DocSale.json')
    # DbModels.LoadMod('DocSale')
    # Ref = DbModels['DocSale']
    # Res1 = await Ref.Add(Data)
    # print(Res1)
    # # Res1 = await Ref.Del(9)
    # print(Res1)

    await Db.Close()
    print('done')

#Test_03()
Task = Test_02()
asyncio.run(Task)
