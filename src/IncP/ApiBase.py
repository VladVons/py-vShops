# Created: 2023.02.02
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.DataClass import DDataClass
from Inc.Loader.Api import TLoaderApi, TLoaderApiFs, TLoaderApiHttp
from Task import LoadClassConf


@DDataClass
class TApiConf():
    master_user: str = ''
    master_password: str = ''
    master_api: str = 'http://host:port/api'
    helper: dict = {}
    dir_module: str = 'IncP/DirName'


class TApiBase():
    def __init__(self):
        self.Conf: TApiConf = None
        self.Master: TLoaderApi = None
        self.ExecCnt = 0

    def GetConf(self) -> dict:
        return LoadClassConf(self)

    def Init(self, aConf: TApiConf):
        raise NotImplementedError()

    def InitMaster(self):
        if (self.Conf.master_api.startswith('http')):
            self.Master = TLoaderApiHttp(self.Conf.master_user, self.Conf.master_password, self.Conf.master_api)
        elif (self.Conf.master_api.startswith('local')):
            self.Master = TLoaderApiFs(self.Conf.master_api)
        else:
            raise ValueError(f'unknown api {self.Conf.master_api}')

    def LoadConf(self):
        Conf = self.GetConf()
        ApiConf = Conf.get('api_conf', {})
        self.Init(TApiConf(**ApiConf))
