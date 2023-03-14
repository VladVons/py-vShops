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
            Path = Val['path']
            if (Path.startswith('http')):
                Loader = TLoaderApiHttp(Val['user'], Val['password'], Path)
            elif (Path.startswith('fs')):
                Loader = TLoaderApiFs(Path)
            else:
                raise ValueError(f'unknown api {Path}')
            self.Loader[Key] = Loader

    def LoadConf(self):
        Conf = self.GetConf()
        ApiConf = Conf.get('api_conf', {})
        self.Init(ApiConf)
