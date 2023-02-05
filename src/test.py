import time
import json
import asyncio
#
from Inc.Db.DbList import TDbSql, TDbList, TDbData
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

def Test_02():
    Fields = [
            ('f1', int),
            ('f2', int),
            ('f3', int),
            ('f4', int)
        ]

    Data1 = []
    for i1 in range(1, 100):
        Data1.append([i1*10+i2 for i2, _ in enumerate(Fields)])

    TimeAt = time.time()
    for i in range(10_000):
        Dbl1 = TDbList(Fields, Data1)
    print(time.time() - TimeAt)

    TimeAt = time.time()
    for i in range(10_000):
        Dbl1 = TDbData(['f1', 'f2', 'f3', 'f4'], Data1)
    print(time.time() - TimeAt)

    # Dbl1.RecAdd()
    # Dbl1.SetField('f2', 111)
    # Dbl1.RecAdd([21, 22, 23, 24])
    # print(Dbl1)

def Test_03():
    Dbl1 = TDbData()
    Dbl1.Load('Temp/ProductDbl-0.json')
    print(Dbl1)

    Dbl1 = TDbList([
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

#Task = Test_02()
#asyncio.run(Task)

Test_02()
