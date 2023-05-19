# Created: 2023.02.13
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.ParserX.Common import TPluginBase
from Inc.Sql import TDbPg, TDbAuth
from .Main import TMain


class TOut_vShopTenant_db(TPluginBase):
    async def Run(self):
        Conf = self.Conf.GetKey('auth')
        DbAuth = TDbAuth(**Conf)
        Db = TDbPg(DbAuth)
        await Db.Connect()

        for Key, Val in self.GetParamDepends().items():
            ParamExport = self.GetParamExport(Key)
            Main = TMain(self, Db, ParamExport)
            await Main.InsertToDb(Val.get('TDbCategory'), Val.get('TDbProductEx'))

        await Db.Close()
