import json
import asyncio
#
from Inc.Misc.Log import TEchoConsoleEx
from Inc.Sql.ADb import TDbAuth
from Task.DbSrv.Api import Api
from IncP.Log import Log

DbAuth = {
    'host': 'localhost',
    'port': 5432,
    'database': 'shop2',
    'user': 'admin',
    'password': '098iop'
}

def LoadJson(aFile: str) -> dict:
    with open(aFile, 'r', encoding = 'utf8') as F:
        Res = json.load(F)
    return Res

async def Test_01():
    Auth = TDbAuth(**DbAuth)
    await Api.DbInit(Auth)

    Data1 = [
        'ref_product/lang',
        {
            "method": "GetProductsWithoutLang",
            "param": [1, 1]
        }
    ]

    Data = LoadJson('Temp/Product.json')
    Data2 = [
        'ref_product',
        {
            "method": "AddProduct",
            "param": [Data]
        }
    ]

    Res = await Api.Exec(*Data1)
    print(Res)

    await Api.DbClose()

Log.AddEcho(TEchoConsoleEx())
Task = Test_01()
asyncio.run(Task)
