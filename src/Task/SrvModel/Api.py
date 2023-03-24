# Created: 2023.02.20
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
#
from Inc.Misc.Time import SecondsToDHMS_Str
from Inc.Sql import TDbExecPool, TDbMeta, TDbPg
from Inc.Sql.ADb import TDbAuth
from Inc.Util.ModHelp import GetHelp, GetMethod
from IncP.ApiBase import TApiBase
from IncP.Plugins import TModels
from IncP.Log import Log, TEchoDb


class TApiModel(TApiBase):
    def __init__(self):
        super().__init__()
        self.DbAuth: TDbAuth = None
        self.DbMeta: TDbMeta = None
        self.Models: TModels = None

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
        self.ExecCnt += 1

        if (not self.Models.IsModule(aModule)):
            if (self.Conf.helper):
                aModule = self.Conf.helper.get('module')
                aData['method'] = self.Conf.helper.get('method')
                aData['param'] = [self.Conf.dir_module]
            else:
                return {'err': f'unknown module {aModule}'}

        self.Models.LoadMod(aModule)
        ModuleObj = self.Models[aModule]

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

    def Init(self, aConf: dict):
        Db = TDbPg(self.DbAuth)
        self.DbMeta = TDbMeta(Db)
        self.Models = TModels(aConf['dir_module'], self.DbMeta)

        #self.Conf.helper = {'module': 'system', 'method': 'Api'}

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

    def LoadConf(self):
        Conf = self.GetConf()

        DbAuth = Conf['db_auth']
        self.DbAuth = TDbAuth(**DbAuth)

        ApiConf = Conf['api_conf']
        self.Init(ApiConf)

ApiModel = TApiModel()
