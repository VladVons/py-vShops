# Created: 2023.03.21
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import time
#
from Inc.Misc.FS import DirWalk


class TCache():
    def __init__(self,
                 aRoot: str = '',
                 aMaxAge: int = 5,
                 aInclModule: list[str] = None,
                 aExclModule: list[str] = None):
        self.MaxAge = aMaxAge
        self.InclModule = aInclModule or []
        self.ExclModule = aExclModule or []
        self.Root = aRoot

    def _Get(self, aPath: str) -> str:
        raise NotImplementedError()

    def _GetAfter(self, _aPath: str, aData: object):
        return aData

    def _GetPath(self, aModule: str, aQuery: dict) -> str:
        if (aQuery):
            #Arr = [f'{Key}:{Val}'for Key, Val in aQuery.items()]
            #File = '_'.join(Arr)
            #File = hash(json.dumps(aQuery))
            File = hex(hash(frozenset(sorted(aQuery))))
        else:
            File = 'index'
        return f'{self.Root}/{aModule}/{File}'

    def _Filter(self, aModule: str) -> bool:
        Res = (not self.MaxAge) or \
              ((self.InclModule) and (aModule not in self.InclModule)) or \
              ((self.ExclModule) and (aModule in self.ExclModule))
        return not Res


    def _Set(self, aPath: str, aData: str):
        raise NotImplementedError()

    def _SetBefore(self, _aPath: str, aData: object):
        return aData

    def Clear(self):
        raise NotImplementedError()

    def Get(self, aModule: str, aQuery: dict) -> str:
        Path = self._GetPath(aModule, aQuery)
        Data = self._Get(Path)
        return self._GetAfter(Path, Data)

    def GetSize(self):
        raise NotImplementedError()

    async def ProxyA(self, aModule: str, aQuery: dict, aFunc: callable, aFuncArgs: list) -> object:
        if (self._Filter(aModule)):
            #Args = tuple(map(aFuncArgs.__getitem__, [1, 2]))
            Res = self.Get(aModule, aQuery)
            if (not Res):
                Res = await aFunc(*aFuncArgs)
                self.Set(aModule, aQuery, Res)
        else:
            Res = await aFunc(*aFuncArgs)
        return Res

    def Set(self, aModule: str, aQuery: dict, aData: str):
        if (self._Filter(aModule)):
            Path = self._GetPath(aModule, aQuery)
            aData = self._SetBefore(Path, aData)
            if (aData):
                self._Set(Path, aData)


class TCacheFile(TCache):
    def _Get(self, aPath: str) -> str:
        if (os.path.exists(aPath)) and (time.time() - os.path.getmtime(aPath) < self.MaxAge):
            with open(aPath, 'r', encoding='utf-8') as F:
                return F.read()

    def _Set(self, aPath: str, aData: str):
        Dir = aPath.rsplit('/', maxsplit=1)[0]
        if (not os.path.isdir(Dir)):
            os.makedirs(Dir)

        with open(aPath, 'w', encoding='utf-8') as F:
            F.write(aData)

    def Clear(self):
        for x in DirWalk(self.Root, aType = 'f'):
            os.remove(x[0])

    def GetSize(self):
        Res = [1 for _x in DirWalk(self.Root, aType = 'f')]
        return (len(Res))


class TCacheMem(TCache):
    Data = {}

    def _Get(self, aPath: str) -> str:
        Data = self.Data.get(aPath)
        if (Data) and (time.time() - Data[1] < self.MaxAge):
            return Data[0]

    def _Set(self, aPath: str, aData: str):
        self.Data[aPath] = (aData, time.time())

    def Clear(self):
        self.Data.clear()

    def GetSize(self):
        return len(self.Data)
