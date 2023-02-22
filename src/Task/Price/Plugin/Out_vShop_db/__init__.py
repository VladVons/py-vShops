# Created: 2023.02.13
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.ParserX.Common import TPluginBase
from Inc.Sql.DbPg import TDbPg
from .Main import TMain


class TOut_vShop_db(TPluginBase):
    async def Run(self):
        DbAuth = self.Conf.GetKey('auth')
        Db = TDbPg(DbAuth)
        await Db.Connect()

        Main = TMain(self, Db)
        DbCategory = self.GetParamDependsIdx('TDbCategory')
        DbProductEx = self.GetParamDependsIdx('TDbProductEx')
        await Main.InsertToDb(DbCategory, DbProductEx)

        await Db.Close()