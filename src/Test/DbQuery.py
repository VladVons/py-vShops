import os
import asyncio
import json
#
from Inc.Sql import TDbPg, TDbAuth, TDbExecPool
from Inc.Misc.Sitemap import TSitemap
from Inc.DbList import TDbList, TDbRec


class TSitemapEx(TSitemap):
    def __init__(self, aDir: str, aUrlRoot: str, aDb):
        super().__init__(aDir, aUrlRoot)
        self.Db = aDb
        # self.MaxRowsRead = 10
        # self.MaxRowsWrite = 50

    async def GetSize(self) -> int:
        Query = '''
            select count(*)
            from ref_product rp
            where enabled and (product0_id is not null)
        '''
        Dbl = await TDbExecPool(self.Db.Pool).Exec(Query)
        return Dbl.Rec.count

    async def GetData(self, aLimit: int, aOffset: int) -> TDbList:
        Query = f'''
            select id, update_date::date
            from ref_product rp
            where enabled and (product0_id is not null)
            limit {aLimit}
            offset {aOffset}
        '''
        Dbl = await TDbExecPool(self.Db.Pool).Exec(Query)
        return Dbl

    async def GetRow(self, aRec: TDbRec) -> str:
        Res = [
            f'  <loc>{self.UrlRoot}/?route=product0/product&product_id={aRec.id}</loc>',
            f'  <lastmod>{aRec.update_date}</lastmod>'
        ]
        return '\n'.join(Res)


async def Connect() -> dict:
    DbAuth = {
        'host': '10.10.1.1',
        'port': 5432,
        'database': 'shop2',
        'user': 'admin',
        'password': '098iop'
    }

    File = 'Conf/Default/Task.SrvModel.Api.json'
    if (os.path.exists(File)):
        with open(File, 'r') as F:
            Data = json.load(F)
            Conf = Data['catalog']['db_auth']
            DbAuth.update(Conf)
    Auth = TDbAuth(**DbAuth)
    Db = TDbPg(Auth)
    await Db.Connect()
    return Db

async def Test_1():
    Db = await Connect()

    Sitemap = TSitemapEx('MVC/catalog/view/sitemap', 'https://used.1x1.com.ua', Db)
    await Sitemap.Create()

    await Db.Close()

Task = Test_1()
asyncio.run(Task)
