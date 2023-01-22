import asyncio
import json
#
from Inc.Util.Obj import DeepSetByList
from Inc.UtilP.Db.DbPg import TDbPg
from Inc.UtilP.Db.DbSql import TDbSql
#from Inc.UtilP.Db.DbModel import TDbModel
#from Inc.Util.Obj import DeepGet, DeepGetRe
from Inc.UtilP.Db.DbMeta import TDbMeta
from Inc.UtilP.Db.DbModel import TDbModel

from IncP.Log import Log
from Inc.UtilP.Log import TEchoConsoleEx, TEchoFileEx
Log.AddEcho(TEchoConsoleEx())


DbAuth = {
    'Server': 'localhost',
    'Database': 'shop2',
    'User': 'admin',
    'Password': '098iop'
}

DataProduct0 = {
    'ref_product0': {
    },
    'ref_product0_image': [
        {
            'image': 'pic1.jpg',
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
        'code': '1234567890125',
        'ident': 'ean'
    },
    'ref_product0_to_category': {
        'category_id    ': 1
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
    #q1 = await TDbSql(Db).Exec("insert into ref_lang (title) values ('test') returning id")
    #q2 = await TDbSql(Db).Exec("select * from ref_lang")

    DbMeta = TDbMeta(Db)
    await DbMeta.Init()

    DbModel = TDbModel('IncP/Db/Model', DbMeta)
    DbModel.LoadMod('RefProduct0')
    await DbModel['RefProduct0'].Add(DataProduct0)

    await Db.Close()
    print('done')


Task = Test_02()
asyncio.run(Task)
