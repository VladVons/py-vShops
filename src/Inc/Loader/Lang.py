# Created: 2023.03.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import json
#
from Inc.Sql import TDbPg, TDbExecPool


class TLoaderLang(dict):
    async def Add(self, aPath: str) -> dict:
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
    def __init__(self, aLang: str, aDirRoot: str):
        self.Dir = f'{aDirRoot}/{aLang}'
        assert (os.path.isdir(self.Dir)), 'Directory not exists'

    async def Add(self, aPath: str) -> dict:
        File = f'{self.Dir}/{aPath}.json'
        if (os.path.exists(File)):
            with open(File, 'r', encoding = 'utf8') as F:
                Data = json.load(F)
        else:
            Data = {}
        self[aPath] = Data
        return Data


class TLoaderLangDb(TLoaderLang):
    def __init__(self, aLang: int, aDb: TDbPg):
        self.Lang = aLang
        self.Db = aDb

    async def Add(self, aPath: str) -> dict:
        pass
