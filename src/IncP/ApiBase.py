# Created: 2023.02.02
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Loader.Api import TLoaderApiFs, TLoaderApiHttp
from Task import LoadClassConf


class TApiBase():
    def __init__(self):
        self.Loader: dict = {}
        self.ExecCnt = 0

    def GetConf(self) -> dict:
        return LoadClassConf(self)

    def Init(self, aConf: dict):
        raise NotImplementedError()

    def InitLoader(self, aConf: dict):
        for Key, Val in aConf.items():
            Type = Val['type']
            if (Type == 'url'):
                Loader = TLoaderApiHttp(Val['user'], Val['password'], Val['url'])
            elif (Type == 'fs'):
                Loader = TLoaderApiFs(Val['module'], Val['class'])
            else:
                raise ValueError(f'unknown type {Type}')
            self.Loader[Key] = Loader

    def LoadConf(self):
        Conf = self.GetConf()
        ApiConf = Conf.get('api_conf', {})
        self.Init(ApiConf)
