# Created: 2023.02.02
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import sys
#
from Inc.DataClass import DDataClass
from Inc.Misc.Request import TRequestJson, TAuth
from Task import LoadClassConf


@DDataClass
class TApiConf():
    master_user: str = ''
    master_password: str = ''
    master_api: str = 'http://host:port/api'
    helper: dict = {}
    dir_module: str = 'IncP/DirName'


class TLoader():
    async def Get(self, aPath: str, aData: dict = None):
        raise NotImplementedError()

class TLoaderLocal(TLoader):
    def __init__(self, aApi: str):
        _Type, Module, Class = aApi.split(':')
        Mod = sys.modules.get(Module)
        self.Api = getattr(Mod, Class)

    async def Get(self, aPath: str, aData: dict = None):
        return await self.Api.Exec(aPath, aData)

class TLoaderHttp(TLoader):
    def __init__(self, aUser: str, aPassword: str, aApiUrl: str):
        Auth = None
        if (aUser):
            Auth = TAuth(aUser, aPassword)
        self.Request = TRequestJson(aAuth=Auth)

        self.ApiUrl = aApiUrl

    async def Get(self, aPath: str, aData: dict = None):
        Url = f'{self.ApiUrl}/{aPath}'
        return await self.Request.Send(Url, aData)


class TApiBase():
    def __init__(self):
        self.Conf: TApiConf = None
        self.Master: TLoader = None
        self.ExecCnt = 0

    def Init(self, aConf: TApiConf):
        raise NotImplementedError()

    def InitMaster(self):
        if (self.Conf.master_api.startswith('http')):
            self.Master = TLoaderHttp(self.Conf.master_user, self.Conf.master_password, self.Conf.master_api)
        elif (self.Conf.master_api.startswith('local')):
            self.Master = TLoaderLocal(self.Conf.master_api)
        else:
            raise ValueError(f'unknown api {self.Conf.master_api}')

    def LoadConf(self):
        Conf = LoadClassConf(self)
        self.Init(TApiConf(**Conf))
