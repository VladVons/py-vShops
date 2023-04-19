# Created: 2023.03.02
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.DataClass import DDataClass
from IncP.ApiBase import TApiBase
from IncP.Plugins import TImgs


@DDataClass
class TExec():
    Method: object
    Module: object


@DDataClass
class TApiImgConf():
    url: str = 'http://localhost:8083/img'
    dir_root: str = 'Data/img'
    dir_route: str = 'MVC/catalog/img'
    dir_thumb: str = 'Data/cache/thumb'
    size_thumb: int = 200
    size_img: int = 1024


class TApiImg(TApiBase):
    def __init__(self):
        super().__init__()
        self.Imgs: TImgs = None
        self.Conf: TApiImgConf = None

    def Init(self, aConf: dict):
        self.Conf = TApiImgConf(**aConf)
        self.Imgs = TImgs(self.Conf.dir_route, self)

    def GetMethod(self, aRoute: str, aData: dict) -> dict:
        if (not self.Imgs.IsModule(aRoute)):
            return {'err': f'Route not found {aRoute}', 'code': 404}

        self.Imgs.LoadMod(aRoute)
        RouteObj = self.Imgs[aRoute]

        Method = aData.get('method', 'Main')
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

        Data = self.GetMethod(aRoute, aData)
        if ('err' in Data):
            return Data

        Param = aData.get('param', {})
        Method, Module = (Data['method'], Data['module'])
        Res = await Method(Module, **Param)
        if (not Res):
            Res = {}
        return Res


ApiImg = TApiImg()
