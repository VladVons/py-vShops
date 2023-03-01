# Created: 2023.02.20
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
#
from Inc.DataClass import DDataClass
from Inc.Misc.Time import SecondsToDHMS_Str
from Inc.Sql.ADb import TDbExecPool
from Inc.Sql.DbPg import TDbPg
from Inc.Sql.DbMeta import TDbMeta
from Inc.Sql.DbModels import TDbModels
from Inc.Util.ModHelp import GetHelp, GetMethod
from IncP.Log import Log, TEchoDb


@DDataClass
class TApiConf():
    dir_module: str = 'IncP/model'
    help: dict = {'module': 'system/help', 'method': 'Api'}

class TApi():
    def __init__(self):
        super().__init__()

        self.Conf: TApiConf
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
            if (self.Conf.help):
                aModule = self.Conf.help.get('module')
                aData['method'] = self.Conf.help.get('method')
                aData['param'] = [self.Conf.dir_module]
            else:
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
        except Exception as E:
            Res = {'err': str(E)}
            Log.Print(1, 'x', 'TApi.Exec()', str(E))
        return Res

    async def DbInit(self, aAuth: dict):
        Db = TDbPg(aAuth)
        await Db.Connect()

        self.DbMeta = TDbMeta(Db)
        await self.DbMeta.Init()
        self.DbModels = TDbModels(self.Conf.dir_module, self.DbMeta)

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

        if (Rec.GetField('tables') == 0):
            Log.Print(1, 'i', 'Database is empty. Creating tables ...')
            await TDbExecPool(self.DbMeta.Db.Pool).ExecFile('IncP/model/vShopsInit.sql')

        Log.AddEcho(TEchoDb(self.DbMeta.Db))

    async def DbClose(self):
        List = Log.FindEcho(TEchoDb.__name__)
        if (List):
            Log.Echoes.remove(List[0])
        await self.DbMeta.Db.Close()

    def Init(self, aConf: TApiConf):
        self.Conf = aConf


Api = TApi()
