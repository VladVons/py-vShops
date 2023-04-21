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
    dir_route: str = 'MVC/catalog/img'
    dir_root: str = 'Data/img'
    dir_thumb: str = 'thumb'
    size_thumb: int = 200
    size_product: int = 1024


class TApiImg(TApiBase):
    def __init__(self):
        super().__init__()

        Conf = self.GetConf()
        self.Conf = TApiImgConf(**Conf)
        self.Imgs = TImgs(self.Conf.dir_route, self)

    async def Exec(self, aRoute: str, aData: dict) -> dict:
        self.ExecCnt += 1

        Data = self.GetMethod(self.Imgs, aRoute, aData)
        if ('err' in Data):
            return Data

        Param = aData.get('param', {})
        Method, Module = (Data['method'], Data['module'])
        Res = await Method(Module, **Param)
        if (not Res):
            Res = {}
        return Res


ApiImg = TApiImg()
