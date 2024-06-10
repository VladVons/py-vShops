# Created: 2024.06.06
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.ParserX.Common import TPluginBase
from Inc.ParserX.CommonSql import TSqlBase
from Inc.Sql import TDbPg, TDbAuth


class TOut_vShopTenantModelUnknown_db(TPluginBase):
    async def Run(self):
        Conf = self.Conf.GetKey('auth')
        DbAuth = TDbAuth(**Conf)
        Db = TDbPg(DbAuth)
        await Db.Connect()

        Sql = TSqlBase(Db)
        Dbl = await Sql.ExecQuery(__package__, 'fmtGet_ModelUnknown2.sql')

        await Db.Close()
        return {'Dbl': Dbl}
