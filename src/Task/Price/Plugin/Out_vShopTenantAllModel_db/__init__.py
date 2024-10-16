# Created: 2023.06.22
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.ParserX.Common import TPluginBase
from Inc.Sql import TDbPg, TDbAuth
from .Main import TMain


class TOut_vShopTenantAllModel_db(TPluginBase):
    async def Run(self):
        Conf = self.Conf.GetKey('auth')
        DbAuth = TDbAuth(**Conf)
        Db = TDbPg(DbAuth)
        await Db.Connect()

        Main = TMain(self, Db)
        Dbl = self.GetParamDependsIdx('TDbCrawl')
        await Main.InsertToDb(Dbl)

        await Db.Close()
