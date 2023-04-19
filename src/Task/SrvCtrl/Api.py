# Created: 2023.03.02
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.DataClass import DDataClass
from Inc.DictDef import TDictKey
from Inc.Loader.Lang import TLoaderLang, TLoaderLangFs
from Inc.Misc.Cache import TCacheMem
from IncP.ApiBase import TApiBase
from IncP.Plugins import TCtrls, TImgs
from IncP.LibCtrl import DeepGetByList, GetDictDef


@DDataClass
class TExec():
    Method: object
    Module: object


class TApiCtrl(TApiBase):
    def __init__(self):
        super().__init__()
        self.Ctrls: TCtrls = None
        self.Imgs: TImgs = None
        self.CacheModel: TCacheMem = None
        self.OnExec: TExec = None
        self.Lang: TLoaderLang = None

    def Init(self, aConf: dict):
        self.Ctrls = TCtrls(aConf['dir_route'], self)
        self.InitLoader(aConf['loader'])

        Data = self.GetMethod('system/session', {'data': {'method': 'OnExec'}})
        assert ('err' not in Data), 'Route not found'
        self.OnExec = TExec(Data['method'], Data['module'])

        Cache = aConf['cache_route']
        self.CacheModel = TCacheMem('/', Cache.get('max_age', 5), Cache.get('incl_route'), Cache.get('excl_route'))

        Section = aConf['lang']
        if (Section['type'] == 'fs'):
            Def = GetDictDef(Section, ['default', 'dir'], ['ua', 'MVC/catalog/lang'])
            self.Lang = TLoaderLangFs(*Def)
        else:
            raise ValueError()

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
        if (not Res):
            Res = {}

        Langs = aData.get('extends', [])
        Langs.append(aData.get('route'))
        for x in Langs:
            await Module.Lang.Add(x)
        Res['lang'] = TDictKey('', Module.Lang.Join())

        Res['modules'] = await Module.LoadModules(aData)
        return Res


ApiCtrl = TApiCtrl()
