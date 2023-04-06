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
        self.Ctrls = TCtrls(aConf['dir_route'], self)
        self.InitLoader(aConf['loader'])

        Data = self.GetMethod('system/session', {'data': {'method': 'OnExec'}})
        assert ('err' not in Data), 'Route not found'
        self.OnExec = TExec(Data['method'], Data['module'])

        Cache = aConf['cache']
        self.CacheModel = TCacheMem('/', Cache.get('max_age', 5), Cache.get('incl_route'), Cache.get('excl_route'))

    def GetMethod(self, aRoute: str, aData: dict) -> dict:
        if (not self.Ctrls.IsModule(aRoute)):
            return {'err': f'Route not found {aRoute}', 'code': 404}

        self.Ctrls.LoadMod(aRoute)
        RouteObj = self.Ctrls[aRoute]

        Method = DeepGetByList(aData, ['data', 'method'], 'Main')
        MethodObj = getattr(RouteObj.Api, Method, None)
        if (MethodObj is None):
            return {'err': f'Method {Method} not found in route {aRoute}', 'code': 404}

        return {'method': MethodObj, 'module': RouteObj}

    async def GetMethodData(self, aRoute: str, aData: dict) -> dict:
        self.ExecCnt += 1
        Data = self.GetMethod(aRoute, aData)
        if ('err' in Data):
            return Data

        Method, Module = (Data['method'], Data['module'])
        return await Method(Module, aData)

    async def Exec(self, aRoute: str, aData: dict) -> dict:
        self.ExecCnt += 1
        if (self.OnExec):
            await self.OnExec.Method(self.OnExec.Module, aData)

        Data = self.GetMethod(aRoute, aData)
        if ('err' in Data):
            return Data

        Method, Module = (Data['method'], Data['module'])
        Res = await Method(Module, aData)
        Res['modules'] = await Module.LoadModules(aData)
        return Res


ApiCtrl = TApiCtrl()
