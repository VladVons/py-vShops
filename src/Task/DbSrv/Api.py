# Created: 2023.02.20
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Misc.Time import SecondsToDHMS_Str
from Inc.Sql.DbPg import TDbPg
from Inc.Sql.DbMeta import TDbMeta
from Inc.Sql.DbModels import TDbModels
from Inc.Util.Mod import GetModuleHelp
from IncP.Log import Log, TEchoDb


class TApi():
    def __init__(self):
        super().__init__()

        self.DbMeta: TDbMeta
        self.DbModels: TDbModels
        self.Cnt = 0

    async def _DoAuthRequest(self, aUser: str, aPassw: str) -> bool:
        #Dbl = await self.Db.UserAuth(aUser, aPassw)
        #return (not Dbl.IsEmpty())
        return True

    async def Exec(self, aModule: str, aData: dict) -> dict:
        self.DbModels.LoadMod(aModule)
        ModuleObj = self.DbModels[aModule]

        if (not aData):
            Data = GetModuleHelp(ModuleObj.Api)
            Help = [[x[4], x[3]] for x in Data]
            return {'err': 'undefined method', 'module': ModuleObj.Api.__file__, 'help': Help}

        if (not self.DbModels.IsModule(aModule)):
            return {'err': f'unknown module {aModule}'}

        Method = aData.get('method')
        if (not Method):
            return {'err': 'undefined method'}

        MethodObj = getattr(ModuleObj.Api, Method, None)
        if (MethodObj is None):
            return {'err': f'unknown method {Method}'}

        Param = aData.get('param', [])
        try:
            if (isinstance(Param, dict)):
                Data = await MethodObj(ModuleObj, **Param)
            else:
                # ParamNeed = MethodObj.__code__.co_varnames[1:MethodObj.__code__.co_argcount]
                # if (len(Param) != len(ParamNeed)):
                #     return {'err': f'param count mismatch. need {ParamNeed} but got {Param}'}
                Data = await MethodObj(ModuleObj, *Param)

            self.Cnt += 1
            Res = {'data': Data, 'cnt': self.Cnt}
        except Exception as E:
            Res = {'err': str(E)}
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
