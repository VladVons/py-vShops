# Created: 2023.05.17
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.ParserX.Common import TPluginBase
from .Main import TCrawl


class TIn_Crawl_model_xlsx(TPluginBase):
    async def Run(self):
        Crawl = TCrawl(self)
        Crawl.InitEngine()
        await Crawl.Load()
        return {'TDbCrawl': Crawl.Dbl}
