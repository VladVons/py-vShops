# Created: 2023.02.02
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Loader.Api import TLoaderApiFs, TLoaderApiHttp
from Inc.Plugin import TPlugin
from Inc.Util.ModHelp import GetHelp, GetMethod
from Task import LoadClassConf


class TApiBase():
    def __init__(self):
        self.ExecCnt = 0
        self.Loader = {}
        self.Cache = {}
        self.AEvent = None
        self.Name = None

    async def ExecOnce(self, aData: dict):
        pass

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

    def GetConf(self) -> dict:
        return LoadClassConf(self)

    def GetMethod(self, aPlugin: TPlugin, aRoute: str, aData: dict) -> dict:
        Method = aData.get('method')

        Key = f'{aRoute}/{Method}'
        Res = aPlugin.Cache.get(Key)
        if (not Res):
            if (not Method):
                return {'err': 'undefined key `method`'}

            if (not aPlugin.IsModule(aRoute)):
                return {'err': f'Route not found {aRoute}', 'code': 404}

            aPlugin.LoadMod(aRoute)
            RouteObj = aPlugin[aRoute]

            MethodObj = getattr(RouteObj.Api, Method, None)
            if (MethodObj is None):
                return {'err': f'Method {Method} not found in route {aRoute}', 'code': 404}

            Res = {'method': MethodObj, 'module': RouteObj}
            aPlugin.Cache[Key] = Res
        return Res

    def InitLoader(self, aConf: dict):
        for Key, Val in aConf.items():
            Type = Val['type']
            if (Type == 'url'):
                Loader = TLoaderApiHttp(Val['user'], Val['password'], Val['url'])
            elif (Type == 'fs'):
                Loader = TLoaderApiFs(Val['module'], Val['class'], self.Name)
            else:
                raise ValueError(f'unknown type {Type}')
            self.Loader[Key] = Loader
