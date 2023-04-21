# Created: 2023.02.20
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Misc.Time import SecondsToDHMS_Str
from Inc.Sql import TDbExecPool, TDbMeta, TDbPg
from Inc.Sql.ADb import TDbAuth
from IncP.ApiBase import TApiBase
from IncP.Plugins import TModels
from IncP.Log import Log, TEchoDb


class TApiModel(TApiBase):
    def __init__(self):
        super().__init__()

        Conf = self.GetConf()
        DbAuth = Conf['db_auth']
        self.DbAuth = TDbAuth(**DbAuth)
        Db = TDbPg(self.DbAuth)
        self.DbMeta = TDbMeta(Db)
        self.Models = TModels(Conf['dir_route'], self.DbMeta)

        self.Helper = {'route': 'system', 'method': 'Api'}

    async def Exec(self, aRoute: str, aData: dict) -> dict:
        self.ExecCnt += 1

        Data = self.GetMethod(self.Models, aRoute, aData)
        if ('err' in Data):
            return Data

        Method, Module = (Data['method'], Data['module'])
        Param = aData.get('param', {})
        Data = await Method(Module, **Param)
        if (Data):
            Res = {'data': Data[0]}
            if (aData.get('query')):
                Res['query'] = Data[1]
        else:
            Res = {'data': None}
        return Res

    async def DbConnect(self):
        await self.DbMeta.Db.Connect()
        await self.DbMeta.Init()

        Dbl = await self.DbMeta.Db.GetDbVersion()
        Version = Dbl.Rec.version.split()[:2]
        Log.Print(1, 'i', 'Server: %s, Uptime: %s, DbName: %s, DbSize: %sM, Tables %s' %
            (
                ' '.join(Version),
                SecondsToDHMS_Str(Dbl.Rec.uptime.seconds),
                Dbl.Rec.db_name,
                round(Dbl.Rec.size / 1000000, 2),
                Dbl.Rec.tables
            )
        )

        if (Dbl.Rec.tables == 0):
            Log.Print(1, 'i', 'Database is empty. Creating tables ...')
            await TDbExecPool(self.DbMeta.Db.Pool).ExecFile(f'{self.Models.Dir}/vShopsMeta.sql')
            await TDbExecPool(self.DbMeta.Db.Pool).ExecFile(f'{self.Models.Dir}/vShopsData.sql')

        Log.AddEcho(TEchoDb(self.DbMeta.Db))

    async def DbClose(self):
        List = Log.FindEcho(TEchoDb.__name__)
        if (List):
            Log.Echoes.remove(List[0])

        if (self.DbMeta):
            await self.DbMeta.Db.Close()


ApiModel = TApiModel()
