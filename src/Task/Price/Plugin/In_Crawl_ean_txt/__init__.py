# Created: 2023.05.18
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.ParserX.Common import TPluginBase
from .Main import TMain


class TIn_Crawl_ean_txt(TPluginBase):
    async def Run(self):
        Main = TMain(self)
        Main.InitEngine()
        await Main.Load()
        return {'TDbCrawl': Main.Dbl}
