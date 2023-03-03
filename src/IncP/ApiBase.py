# Created: 2023.02.02
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.DataClass import DDataClass
from Inc.Misc.Request import TRequestJson, TAuth


@DDataClass
class TApiConf():
    master_user: str = ''
    master_password: str = ''
    master_api: str = 'http://host:port/api'
    helper: dict = {}
    dir_module: str = 'IncP/DirName'


class TLoader():
    async def Get(self, aPath: str, aQuery: str):
        raise NotImplementedError()

class TLoaderLocal(TLoader):
    def __init__(self, aApiDir: str):
        self.ApiDir = aApiDir

    async def Get(self, aPath: str, aQuery: str):
        pass

class TLoaderHttp(TLoader):
    def __init__(self, aUser: str, aPassword: str, aApiUrl: str):
        Auth = None
        if (aUser):
            Auth = TAuth(aUser, aPassword)
        self.Request = TRequestJson(aAuth=Auth)

        self.ApiUrl = aApiUrl

    async def Get(self, aPath: str, aQuery: str):
        Url = f'{self.ApiUrl}/{aPath}?{aQuery}'
        return await self.Request.Send(Url, {})


class TApiBase():
    def __init__(self):
        self.Conf: TApiConf = None
        self.Master: TLoader = None
        self.ExecCnt = 0

    def Init(self, aConf: TApiConf):
        raise NotImplementedError()
