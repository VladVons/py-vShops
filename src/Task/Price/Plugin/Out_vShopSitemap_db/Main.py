# Created: 2023.02.13
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
#
from Inc.DbList import TDbList, TDbRec
from Inc.DataClass import DDataClass
from Inc.ParserX.Common import TFileBase
from Inc.Sql import TDbExecPool, TDbPg
from Inc.Misc.Sitemap import TSitemap
from Inc.Misc.Template import FormatFile


class TSitemapEx(TSitemap):
    def __init__(self, aDir: str, aDb: TDbPg, aUrlRoot: str, aMaxRow: int = 1000):
        super().__init__(aDir, aUrlRoot, aMaxRow)
        self.Db = aDb

    async def GetSize(self) -> int:
        Query = '''
            select
                count(*) as cnt
            from
                ref_product_to_category
        '''
        Dbl = await TDbExecPool(self.Db.Pool).Exec(Query)
        return Dbl.Rec.cnt

    async def GetData(self, aLimit: int, aOffset: int) -> TDbList:
        Dir = __package__.replace('.', '/')
        Query = FormatFile(f'{Dir}/fmtGet_Tenant_Sitemap.sql', {'aLimit': aLimit, 'aOffset': aOffset})
        return await TDbExecPool(self.Db.Pool).Exec(Query)

    async def GetRow(self, aRec: TDbRec) -> str:
        Path = '0_' + '_'.join(map(str, aRec.path_idt))
        Res = f'?route=product/product&path={Path}&product_id={aRec.product_id}&tenant={aRec.tenant_id}'
        return Res


@DDataClass
class TSqlConf():
    url_root: str
    lang_id: int
    parts: int = 100

class TMain(TFileBase):
    async def Exec(self, aDb: TDbPg):
        SqlDef = self.Parent.Conf.GetKey('sql', {})
        SqlConf = TSqlConf(**SqlDef)

        Dir = self.Parent.Conf.get('dir')
        os.makedirs(Dir, exist_ok=True)
        Sitemap = TSitemapEx(Dir, aDb, SqlConf.url_root, SqlConf.parts)
        await Sitemap.Create()
