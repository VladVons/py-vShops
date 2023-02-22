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

Data1 = [
    'ref_product/lang',
    {
        "method": "GetProductsWithoutLang",
        "param": [1, 1]
    }
]

Data2 = [
    'ref_product/category',
    {
        "method": "GetCategoriesByParent",
        "param": [1, 0, 1]
    }
]

Data = LoadJson('Temp/Product.json')
Data3 = [
    'ref_product',
    {
        "method": "AddProduct",
        "param": [Data]
    }
]

async def Test_01():
    Auth = TDbAuth(**DbAuth)
    await Api.DbInit(Auth)

    Res = await Api.Exec(*Data2)
    if ('err' not in Res):
        Dbl = TDbList().Import(Res.get('data'))
        print(Dbl)

    await Api.DbClose()

Log.AddEcho(TEchoConsoleEx())
Task = Test_01()
asyncio.run(Task)
