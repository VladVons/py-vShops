# Created: 2023.05.25
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.ParserX.Common import TPluginBase
from .Main import TMain


class TIn_Crawl_kalina_xls(TPluginBase):
    async def Run(self):
        Main = TMain(self)
        Main.InitEngine()
        await Main.Load()
        return {'TDbCrawl': Main.Dbl}
