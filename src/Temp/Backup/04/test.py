import time
import json
import asyncio
#
from Inc.DbList import TDbSql, TDbListSafe, TDbList
from Inc.Sql.DbPg import TDbPg
from Inc.Sql.DbMeta import TDbMeta
from Inc.Sql.DbModels import TDbModels
from Inc.Sql.DbModel import TDbModel
#
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


def Test_01():
    Data = LoadJson('Temp/ProductDbl-1.json')
    Dbl = TDbSql()
    for x in Data:
        Dbl.Import(x)
        print(Dbl)

def Test_02():
    Fields = [
        ('f1', int),
        ('f2', int),
        ('f3', int)
    ]

    Rows = 10
    Data1 = []
    for i1 in range(1, Rows):
        Data1.append([i1*10+i2 for i2, _ in enumerate(Fields)])

    # Dbl1 = TDbList(['f1', 'f2', 'f3'], Data1)
    # for i, x in enumerate(Dbl1):
    #     x.SetField('f3', str(1000 + i))
    #     d1 = x.GetField('f2')
    #     d2 = x.GetAsDict()
    #     d3 = x.GetAsSql()
    #     d4 = x.GetAsTuple()
    # Dbl1.RecAdd([100, 200, 300])
    # #x = Dbl1.RecGo(1)
    # x = Dbl1.RecPop()
    # print(Dbl1)
    # pass

    TimeAt = time.time()
    Dbl1 = TDbList(['f1', 'f2', 'f3'], Data1)
    q1 = Dbl1.New()
    for i in range(10_000):
        q1 = Dbl1.Rec.GetAsSql()
        #Dbl1.Rec.GetAsDict()
        # for Rec in Dbl1:
        #     q1 = Rec.GetAsSql()
    print(time.time() - TimeAt)

    TimeAt = time.time()
    Dbl1 = TDbListSafe()
    Dbl1.OptSafe = False
    Dbl1.Init(Fields, Data1)
    for i in range(10_000):
        q1 = Dbl1.Rec.GetAsSql()
        # Dbl1.Rec.GetAsDict()
        # for Rec in Dbl1:
        #     q1 = Rec.GetAsSql()
    print(time.time() - TimeAt)

    # Dbl1.RecAdd()
    # Dbl1.SetField('f2', 111)
    # Dbl1.RecAdd([21, 22, 23, 24])
    # print(Dbl1)

def Test_03():
    Dbl1 = TDbList()
    Dbl1.Load('Temp/ProductDbl-0.json')
    print(Dbl1)

    Dbl1 = TDbListSafe([
        ('User', str),
        ('Age', int),
        ('Male', bool, True),
        ('Price', float)
    ])

    Data = [
        ['User5', 55, True, 5.67],
        ['User2', 22, True, 2.34],
        ['User6', 66, True, 6.78],
        ['User1', 11, False, 1.23],
        ['User3', 33, True, 3.45],
        ['User4', 44, True, 4.56],
        ['User5', 55, True, 5.55]
    ]
    Dbl1.SetData(Data)

    print(Dbl1)


async def Test_04():
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
    # Res1 = await Ref.Del(199)
    # print(Res1)

    # Data = LoadJson('Temp/Product0A.json')
    # DbModels.LoadMod('RefProduct0')
    # Ref = DbModels['RefProduct0']
    # Res1 = await Ref.AddList(Data)
    # print(Res1)
    # Res1 = await Ref.Del(199)
    # print(Res1)

    # Data = LoadJson('Temp/Product0Category.json')
    # DbModels.LoadMod('RefProduct0Category')
    # Ref = DbModels['RefProduct0Category']
    # Res1 = await Ref.Add(Data)
    # print(Res1)

    # Data = LoadJson('Temp/Product0CategoryA.json')
    # SaveJson('Temp/Product0CategoryA-Min.json', Data, False)
    # SaveJson('Temp/Product0CategoryA-Max.json', Data, True)
    # DbModels.LoadMod('RefProduct0Category')
    # Ref = DbModels['RefProduct0Category']
    # Res1 = await Ref.AddList(Data)
    # print(Res1)

    # Data = LoadJson('Temp/Product.json')
    # DbModels.LoadMod('RefProduct')
    # Ref = DbModels['RefProduct']
    # Res1 = await Ref.Add(Data)
    # print(Res1)
    # Res1 = await Ref.Del(14)
    # print(Res1)

    # Data = LoadJson('Temp/DocSale.json')
    # DbModels.LoadMod('DocSale')
    # Ref = DbModels['DocSale']
    # Res1 = await Ref.Add(Data)
    # print(Res1)
    # # Res1 = await Ref.Del(9)
    # print(Res1)

    await Db.Close()
    print('done')

Task = Test_04()
asyncio.run(Task)
