import json
import asyncio

from Inc.DbList import TDbList
from Inc.Misc.Log import TEchoConsoleEx
# from Inc.Misc.Request import TRequestJson
from Inc.Sql.ADb import TDbAuth
from Task.SrvModel.Api import ApiModel
from Task.SrvCtrl.Api import ApiCtrl
from IncP.Log import Log


def LoadJson(aFile: str) -> dict:
    with open(aFile, 'r', encoding = 'utf8') as F:
        Res = json.load(F)
    return Res

DbAuth = {
    'host': '5.58.6.236',
    'port': 5432,
    'database': 'shop2',
    'user': 'admin',
    'password': '098iop'
}

def LoadData() -> str:
    Json = LoadJson('Temp/Product.json')

    Res = [
        'ref_product',
        {
            "method": "AddProduct",
            "param": [Json]
        }
    ]
    return Res

Data2 = [
    'ref_product/lang',
    {
        "method": "GetProductsWithoutLang",
        "param": [1, 1]
    }
]

Data3a = [
    'ref_product/category',
    {
        "method": "GetCategoriesByParent",
        "param": [1, 0, 3]
    }
]

Data3b = [
    'ref_product/category',
    {
        "method": "GetProductsCountAndNameInCategories",
        "param": [1, 1]
    }
]

Data3c = [
    'ref_product/category',
    {
        "method": "GetCategoriesByParentWithProductCount",
        "param": [1, 0]
    }
]

Data4 = [
    'ref_product',
    {
        "method": "GetProducts",
        "param": [1, '15 03']
    }
]

Data5 = [
    'ref_product',
    {
        "method": "AddHistProductSearch",
        "param": [1, 1, '15 03']
    }
]

async def Test_01():
    ApiModel.LoadConf()
    ApiModel.Auth = TDbAuth(**DbAuth)
    await ApiModel.DbConnect()

    #for xData in [Data2, Data3a, Data3b, Data3c, Data4, Data5]:
    for xData in [Data3a]:
        Res = await ApiModel.Exec(*xData)
        if ('err' in Res):
            print(Res)
        else:
            Data = Res.get('data')
            if (Data):
                if ('head' in Data):
                    Dbl = TDbList().Import(Data)
                    Dbl.OptReprLen = 60
                    print(Dbl)
                else:
                    print(Data)

    await ApiModel.DbClose()


async def Test_02():
    Request = TRequestJson()
    Res1 = await Request.Send(
        'http://localhost:8081/api/ref_product',
        {
            "method": "GetProducts",
            "param": [
                1,
                "220 (60"
            ]
        }
    )
    print(Res1)

async def Test_03():
    ApiModel.LoadConf()
    ApiModel.Auth = TDbAuth(**DbAuth)
    await ApiModel.DbConnect()
    Res = await ApiModel.Exec(*Data3a)


    ApiCtrl.LoadConf()
    Res = await ApiCtrl.Exec('common/home', {'method': 'Main'})
    pass


def Test_04():
    D1 = {
        'd1' : {'one': 1, 'two': 2},
        'd2': {'sunday':0, 'monday': 1},
        'd3': {'one':11}
    }

    Res = {}
    #L1 = list(D1.values())
    #r1 = {x for x in L1}
    #Res.update(D1['d1'])
    #Res = {Res | dict(**x) for x in L1}
    #print(Res)


Log.AddEcho(TEchoConsoleEx())
Task = Test_03()
asyncio.run(Task)
