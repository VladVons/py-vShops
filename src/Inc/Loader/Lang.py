# Created: 2023.03.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import json
#
from Inc.Sql import TDbPg, TDbExecPool


class TLoaderLang(dict):
    async def Add(self, aLang: str, aPath: str, aKey: str) -> dict:
        raise NotImplementedError()

    def Get(self, aKey: str) -> str:
        return self.get(aKey, f'-{aKey}-')

    def Join(self) -> dict:
        # ToDo # Res.update(*list(self.values()))
        Res = {}
        for x in self.values():
            Res.update(x)
        return Res


class TLoaderLangFs(TLoaderLang):
    def __init__(self, aDirRoot: str):
        assert(os.path.isdir(aDirRoot)), f'Directory not exists {aDirRoot}'

        self.Common = '__init__'
        self.DirRoot = aDirRoot

    async def Add(self, aLang: str, aPath: str, aKey: str = 'tpl') -> dict:
        Res = {}
        Common = aPath.rsplit('/', maxsplit=1)[0] + '/' + self.Common
        for xPath in [Common, aPath]:
            File = f'{self.DirRoot}/{aLang}/{xPath}.json'
            if (os.path.exists(File)):
                with open(File, 'r', encoding = 'utf8') as F:
                    Data = json.load(F)
                    Res.update(Data.get(aKey, {}))
        self[aPath] = Res
        return Res


class TLoaderLangDb(TLoaderLang):
    def __init__(self, aLang: int, aDb: TDbPg):
        self.Lang = aLang
        self.Db = aDb

    async def Add(self, aPath: str) -> dict:
        pass
