# Created: 2023.05.25
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.ParserX.Common import TPluginBase
from .Main import TMain


class TIn_Crawl_fozzy_sqlite(TPluginBase):
    async def Run(self):
        Main = TMain(self)
        Main.InitEngine()

        Query = '''
            select
                barcode as ean,
                path as category,
                name as product,
                url,
                urls as images,
                info as descr,
                opt as features
            from
                data_ua
            where (img > 0)
        '''
        Main.SetSheet(Query)

        await Main.Load()
        return {'TDbCrawl': Main.Dbl}
