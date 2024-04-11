# Created: 2023.03.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import sys
from urllib.parse import urlparse
#
#from Inc.Misc.Misc import TJsonEncoder
from Inc.Misc.Request import TRequestJson, TAuth
from Inc.Util.Obj import DeepGetByList

class TLoaderApi():
    async def Get(self, aPath: str, aData: dict = None):
        raise NotImplementedError()


class TLoaderApiFs(TLoaderApi):
    def __init__(self, aModule: str, aClass: str, aName: str = None):
        Mod = sys.modules.get(aModule)
        if (Mod is None):
            __import__(aModule)
            Mod = sys.modules.get(aModule)

        self.Api = getattr(Mod, aClass)
        if (aName):
            self.Api = self.Api[aName]

    async def Get(self, aPath: str, aData: dict = None):
        Res = await self.Api.Exec(aPath, aData)
        #return TJsonEncoder.Dumps(Res) #ToDo
        return Res


class TLoaderApiHttp(TLoaderApi):
    def __init__(self, aUser: str, aPassword: str, aApiUrl: str, aName: str = None):
        self.Name = aName

        Auth = None
        if (aUser):
            Auth = TAuth(aUser, aPassword)

        Parts = urlparse(aApiUrl)
        Root = f'{Parts.scheme}://{Parts.netloc}'
        self.Api = Parts.path

        self.Request = TRequestJson(Root, Auth)

    async def Get(self, aPath: str, aData: dict = None):
        if (self.Name):
            aData = aData or {}
            aData['_path'] = self.Name

        Path = f'{self.Api}/{aPath}'
        Res = await self.Request.Send(Path, aData)
        return DeepGetByList(Res, ['data', 'data'], Res)
