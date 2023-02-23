# Created: 2023.02.20
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
#
from Inc.Misc.Time import SecondsToDHMS_Str
from Inc.Sql.DbPg import TDbPg
from Inc.Sql.DbMeta import TDbMeta
from Inc.Sql.DbModels import TDbModels
from Inc.Util.ModHelp import GetHelp, GetMethod
from IncP.Log import Log, TEchoDb


class TApi():
    def __init__(self):
        super().__init__()

        self.DbMeta: TDbMeta
        self.DbModels: TDbModels
        self.QueryCnt = 0

    async def _DoAuthRequest(self, aUser: str, aPassw: str) -> bool:
        #Dbl = await self.Db.UserAuth(aUser, aPassw)
        #return (not Dbl.IsEmpty())
        return True

    @staticmethod
    def _GetMethodHelp(aMod: object, aMethod: str) -> dict:
        Obj = getattr(aMod, aMethod, None)
        if (Obj is None):
            Res = {
                'err': f'unknown method {aMethod}',
                'help': GetHelp(aMod)
            }
        else:
            Data = GetMethod(Obj)
            Res = {
                'help': {'decl': Data[2],
                'doc': Data[3]}
            }
        return Res

    async def Exec(self, aModule: str, aData: dict) -> dict:
        self.QueryCnt += 1

        if (not self.DbModels.IsModule(aModule)):
            return {'err': f'unknown module {aModule}'}

        self.DbModels.LoadMod(aModule)
        ModuleObj = self.DbModels[aModule]

        if (not aData):
            return {'err': 'undefined data'}

        Method = aData.get('method')
        if (not Method):
            return {'err': 'undefined key `method`'}

        if (Method.startswith('Help ')):
            Method = re.split(r'\s+', Method)[1]
            return self._GetMethodHelp(ModuleObj.Api, Method)

        MethodObj = getattr(ModuleObj.Api, Method, None)
        if (MethodObj is None):
            return {
                'err': f'unknown method {Method}',
                'help': GetHelp(ModuleObj.Api),
            }

        Param = aData.get('param', [])
        try:
            if (isinstance(Param, dict)):
                Data = await MethodObj(ModuleObj, **Param)
            else:
                Data = await MethodObj(ModuleObj, *Param)
            Res = {'data': Data}
        except TypeError as E:
            Log.Print(1, 'x', 'TApi.Exec()', str(E))
        except Exception as E:
            Res = {'err': str(E)}
            Log.Print(1, 'x', 'TApi.Exec()', str(E))
        return Res

    async def DbInit(self, aAuth: dict):
        Db = TDbPg(aAuth)
        await Db.Connect()
        # await self.Db.ExecFile('IncP/DB/Scraper_pg.sql')

        self.DbMeta = TDbMeta(Db)
        await self.DbMeta.Init()
        self.DbModels = TDbModels('IncP/model', self.DbMeta)

        Dbl = await self.DbMeta.Db.GetDbVersion()
        Rec = Dbl.Rec
        Version = Rec.GetField('version').split()[:2]
        Uptime = Rec.GetField('uptime')
        Log.Print(1, 'i', 'Server: %s, Uptime: %s, DbName: %s, DbSize: %sM, Tables %s' %
            (
                ' '.join(Version),
                SecondsToDHMS_Str(Uptime.seconds),
                Rec.GetField('db_name'),
                round(Rec.GetField('size') / 1000000, 2),
                Rec.GetField('tables'))
            )

        Log.AddEcho(TEchoDb(self.DbMeta.Db))

    async def DbClose(self):
        List = Log.FindEcho(TEchoDb.__name__)
        Log.Echoes.remove(List[0])
        await self.DbMeta.Db.Close()

Api = TApi()
