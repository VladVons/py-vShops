import json
import asyncio
#
from Inc.UtilP.Db.DbPg import TDbPg
from Inc.UtilP.Log import TEchoConsoleEx
from Inc.UtilP.Db.DbMeta import TDbMeta
from Inc.UtilP.Db.DbModels import TDbModels


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

async def Test_02():
    Db = TDbPg(DbAuth)
    await Db.Connect()

    #q1 = await Db.Exec("insert into ref_lang (title) values ('test')")
    #q2 = await Db.Exec("select * from ref_lang")

    DbMeta = TDbMeta(Db)
    await DbMeta.Init()
    DbModels = TDbModels('IncP/Db/Model', DbMeta)

    # Product0 = LoadJson('Temp/Product0.json')
    # DbModels.LoadMod('RefProduct0')
    # Ref = DbModels['RefProduct0']
    # Res1 = await Ref.Add(Product0)
    # print(Res1)

    # Product0L = LoadJson('Temp/Product0A.json')
    # DbModels.LoadMod('RefProduct0')
    # Ref = DbModels['RefProduct0']
    # #Res1 = await Ref.AddList(Product0L)
    # #print(Res1)
    # Res1 = await Ref.Del(199)
    # print(Res1)

    # Product0Category = LoadJson('Temp/Product0Category.json')
    # DbModels.LoadMod('RefProduct0Category')
    # Ref = DbModels['RefProduct0Category']
    # Res1 = await Ref.Add(Product0Category)
    # print(Res1)

    Product0Category = LoadJson('Temp/Product0CategoryA.json')
    DbModels.LoadMod('RefProduct0Category')
    Ref = DbModels['RefProduct0Category']
    Res1 = await Ref.AddList(Product0Category)
    print(Res1)


    await Db.Close()
    print('done')

#Test_03()
Task = Test_02()
asyncio.run(Task)
