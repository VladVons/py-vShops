# Created: 2023.03.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import sys
#
from Inc.Misc.Request import TRequestJson, TAuth


class TLoaderApi():
    async def Get(self, aPath: str, aData: dict = None):
        raise NotImplementedError()

class TLoaderApiFs(TLoaderApi):
    def __init__(self, aApi: str):
        _Type, Module, Class = aApi.split(':')
        Mod = sys.modules.get(Module)
        if (Mod is None):
            __import__(Module)
            Mod = sys.modules.get(Module)
        self.Api = getattr(Mod, Class)

    async def Get(self, aPath: str, aData: dict = None):
        return await self.Api.Exec(aPath, aData)

class TLoaderApiHttp(TLoaderApi):
    def __init__(self, aUser: str, aPassword: str, aApiUrl: str):
        Auth = None
        if (aUser):
            Auth = TAuth(aUser, aPassword)
        self.Request = TRequestJson(aAuth=Auth)

        self.ApiUrl = aApiUrl

    async def Get(self, aPath: str, aData: dict = None):
        Url = f'{self.ApiUrl}/{aPath}'
        return await self.Request.Send(Url, aData)
