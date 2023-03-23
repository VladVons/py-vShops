# Created: 2023.03.02
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.DataClass import DDataClass
from Inc.Util.Obj import DeepGetByList
from Inc.Misc.Cache import TCacheMem
from IncP.ApiBase import TApiBase
from IncP.Plugins import TCtrls


@DDataClass
class TExec():
    Method: object
    Module: object


class TApiCtrl(TApiBase):
    def __init__(self):
        super().__init__()
        self.Ctrls: TCtrls = None
        self.CacheModel: TCacheMem = None
        self.OnExec: TExec = None

    def Init(self, aConf: dict):
        self.Ctrls = TCtrls(aConf['dir_module'], self)
        self.InitLoader(aConf['loader'])

        Data = self.GetMethod('system/session', {'data': {'method': 'OnExec'}})
        assert ('err' not in Data), 'Module not found'
        self.OnExec = TExec(Data['method'], Data['module'])

        Cache = aConf['cache']
        self.CacheModel = TCacheMem('/', Cache.get('max_age', 5), Cache.get('incl_module'), Cache.get('excl_module'))

    def GetMethod(self, aModule: str, aData: dict) -> dict:
        if (not self.Ctrls.IsModule(aModule)):
            return {'err': f'Module not found {aModule}', 'code': 404}

        self.Ctrls.LoadMod(aModule)
        ModuleObj = self.Ctrls[aModule]

        Method = DeepGetByList(aData, ['data', 'method'], 'Main')
        MethodObj = getattr(ModuleObj.Api, Method, None)
        if (MethodObj is None):
            return {'err': f'Method {Method} not found in module {aModule}', 'code': 404}

        return {'method': MethodObj, 'module': ModuleObj}

    async def Exec(self, aModule: str, aData: dict) -> dict:
        self.ExecCnt += 1

        Data = self.GetMethod(aModule, aData)
        if ('err' in Data):
            return Data

        if (self.OnExec):
            await self.OnExec.Method(self.OnExec.Module, aData)

        Method, Module = (Data['method'], Data['module'])
        return await Method(Module, aData)


ApiCtrl = TApiCtrl()
