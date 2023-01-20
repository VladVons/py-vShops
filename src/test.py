import asyncio
import json
#
from Inc.UtilP.Db.DbPg import TDbPg
#from Inc.UtilP.Db.DbModel import TDbModel
from Inc.UtilP.Db.DbMeta import TDbMeta
from Inc.UtilP.Db.DbModel import TDbModel

#from Inc.Util.Obj import DeepGet, DeepGetRe

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
    'ref_product0_lang': {
        'title' : 'Title1',
        'descr': 'Descr1',
        'lang_id': 1
    },
    'ref_product0_barcode': {
        'code': '1234567890123',
        'ident': 'ean'
    },
    'ref_product0_to_category': {
        'category_id': 1
    },
    'ref_product0_crawl': {
        'url': 'http://example.com',
        'ident': 'ean',
        'code': '1234567890123',
        'succsess': True
    }
}


async def Test_01():
    Db = TDbPg(DbAuth)
    await Db.Connect()

    DbMeta = TDbMeta(Db)
    await DbMeta.Init()

    #DbModel = TDbModelMain(DbAuth)
    #DbMeta = TDbMeta('IncP/Db/Model')
    #DbMeta.Sort()
    #DbMeta.Create()
    #DbMeta.LoadModel('DocSale')
    #for i, x in enumerate(DbMeta.Tables):
    #    print(i+1, x)
    #pass
    #DbSql = await DbModel.Add(Data)

    await Db.Close()

async def Test_02():
    Db = TDbPg(DbAuth)
    await Db.Connect()

    DbMeta = TDbMeta(Db)
    await DbMeta.Init()

    DbModel = TDbModel('IncP/Db/Model', Db)
    DbModel.LoadMod('RefProduct0')
    await DbModel['RefProduct0'].Add(DataProduct0)

    await Db.Close()
    print('done')


Task = Test_02()
asyncio.run(Task)
