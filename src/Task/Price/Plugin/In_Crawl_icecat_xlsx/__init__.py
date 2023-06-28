# Created: 2023.06.22
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.ParserX.Common import TPluginBase
from .Main import TMain


class TIn_Crawl_icecat_xlsx(TPluginBase):
    async def Run(self):
        Main = TMain(self)
        Main.InitEngine()

        #Main.SetSheet('computer')
        await Main.Load()
        #await Main.Load(aSave = False)
        #Main.SetSheet('monitor')
        #await Main.Load()

        return {'TDbCrawl': Main.Dbl}
