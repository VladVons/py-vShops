import time
import asyncio
import json
#
from Inc.UtilP.Db.DbPg import TDbPg
from Inc.UtilP.Log import TEchoConsoleEx
from Inc.UtilP.Db.DbMeta import TDbMeta
from Inc.UtilP.Db.DbModel import TDbModel
from Inc.Util.Obj import DeepGetsRe, DeepGets, DeepGetByList
from Inc.Db.DbList import TDbList

from IncP.Log import Log
Log.AddEcho(TEchoConsoleEx())


DbAuth = {
    'Server': 'localhost',
    'Database': 'shop2',
    'User': 'admin',
    'Password': '098iop'
}
    # 'ref_product1': {
    # },

DataProduct0 = {
    'ref_product0_image': [
        {
            'image': 'pic2.jpg',
            'sort_order': 1
        },
        {
            'image': 'pic2.jpg',
            'sort_order': 2
        }
    ],
    'ref_product0_lang': [
        {
            'title' : 'Title1',
            'descr': 'Descr1',
            'lang_id': 1
        }
    ],
    'ref_product0_barcode': {
        'code': '1234567890137',
        'ident': 'ean'
    },
    'ref_product0_crawl': {
        'url': 'http://example.com',
        'ident': 'ean',
        'code': '1234567890110',
        'succsess': True,
        'crawl_site_id': 1
    }
}


async def Test_02():
    Db = TDbPg(DbAuth)
    await Db.Connect()

    #q1 = await Db.Exec("insert into ref_lang (title) values ('test')")
    #q2 = await Db.Exec("select * from ref_lang")

    DbMeta = TDbMeta(Db)
    await DbMeta.Init()

    DbModel = TDbModel('IncP/Db/Model', DbMeta)
    DbModel.LoadMod('RefProduct0')
    Res1 = await DbModel['RefProduct0'].Add(DataProduct0)
    print(Res1)

    await Db.Close()
    print('done')

#Test_03()
Task = Test_02()
asyncio.run(Task)
