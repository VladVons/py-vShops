import json
import asyncio
#
from Inc.DbList import TDbList
from Inc.Misc.Log import TEchoConsoleEx
from Inc.Sql.ADb import TDbAuth
from Task.DbSrv.Api import Api
from IncP.Log import Log


def LoadJson(aFile: str) -> dict:
    with open(aFile, 'r', encoding = 'utf8') as F:
        Res = json.load(F)
    return Res

DbAuth = {
    'host': 'localhost',
    'port': 5432,
    'database': 'shop2',
    'user': 'admin',
    'password': '098iop'
}

Json = LoadJson('Temp/Product.json')
Data1 = [
    'ref_product',
    {
        "method": "AddProduct",
        "param": [Json]
    }
]

Data2 = [
    'ref_product/lang',
    {
        "method": "GetProductsWithoutLang",
        "param": [1, 1]
    }
]

Data3 = [
    'ref_product/category',
    {
        "method": "GetCategoriesByParent",
        "param": [1, 0, 3]
    }
]

Data3a = [
    'ref_product/category',
    {
        "method": "GetProductsCountAndNameInCategories",
        "param": [1, 1]
    }
]

Data3b = [
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
    Auth = TDbAuth(**DbAuth)
    await Api.DbInit(Auth)

    Res = await Api.Exec(*Data3)
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

    await Api.DbClose()

Log.AddEcho(TEchoConsoleEx())
Task = Test_01()
asyncio.run(Task)
