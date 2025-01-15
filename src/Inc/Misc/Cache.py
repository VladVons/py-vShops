# Created: 2023.03.21
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import time
#
from Inc.Misc.FS import DirWalk
from Inc.Misc import Serialize


class TCache():
    def __init__(self, aMaxAge: int = 5, aInclModule: list[str] = None, aExclModule: list[str] = None):
        self.MaxAge = aMaxAge
        self.InclModule = aInclModule or []
        self.ExclModule = aExclModule or []

    def _Get(self, aPath: str) -> str:
        raise NotImplementedError()

    def _GetAfter(self, _aPath: str, aData: object):
        return aData

    def _Set(self, aPath: str, aData: str):
        raise NotImplementedError()

    def Clear(self, aAge: int):
        raise NotImplementedError()

    def GetSize(self):
        raise NotImplementedError()

    def _SetBefore(self, _aPath: str, aData: object):
        return aData

    def _GetPath(self, aRoute: str, aQuery: dict = None) -> str:
        if (aQuery):
            #Arr = [f'{Key}:{Val}'for Key, Val in aQuery.items()]
            #File = '_'.join(Arr)
            #File = hash(json.dumps(aQuery))
            Str = f'{self.MaxAge}/{aRoute}/{sorted(aQuery.items())}'
        else:
            Str = f'{self.MaxAge}/{aRoute}'
        return hex(abs(hash(Str)))

    def _Filter(self, aRoute: str) -> bool:
        Res = (not self.MaxAge) or \
              ((self.InclModule) and (aRoute not in self.InclModule)) or \
              ((self.ExclModule) and (aRoute in self.ExclModule))
        return not Res

    def Get(self, aRoute: str, aQuery: dict = None) -> str:
        Path = self._GetPath(aRoute, aQuery)
        Data = self._Get(Path)
        return self._GetAfter(Path, Data)

    async def ProxyA(self, aRoute: str, aQuery: dict, aFunc: callable, aFuncArgs: list = None) -> object:
        if (self._Filter(aRoute)):
            #Args = tuple(map(aFuncArgs.__getitem__, [1, 2]))
            Res = self.Get(aRoute, aQuery)
            if (not Res):
                if (aFuncArgs):
                    Res = await aFunc(*aFuncArgs)
                else:
                    Res = await aFunc()
                self.Set(aRoute, aQuery, Res)
        else:
            Res = await aFunc(*aFuncArgs)
        return Res

    def Set(self, aRoute: str, aQuery: dict, aData: str):
        if (self._Filter(aRoute)):
            Path = self._GetPath(aRoute, aQuery)
            aData = self._SetBefore(Path, aData)
            if (aData):
                self._Set(Path, aData)


class TCacheFile(TCache):
    def __init__(self,
        aRoot: str = '/tmp/cache',
        aMaxAge: int = 5,
        aInclModule: list[str] = None,
        aExclModule: list[str] = None
    ):
        super().__init__(aMaxAge, aInclModule, aExclModule)
        self.Root = aRoot

    def _GetPath(self, aRoute: str, aQuery: dict = None) -> str:
        Hash = super()._GetPath(aRoute, aQuery)
        return f'{self.Root}/{Hash}'

    def _Get(self, aPath: str) -> str:
        if (os.path.exists(aPath)) and (time.time() - os.path.getmtime(aPath) < self.MaxAge):
            return Serialize.ReadFile(aPath)

    def _Set(self, aPath: str, aData: object):
        Dir = aPath.rsplit('/', maxsplit=1)[0]
        if (not os.path.isdir(Dir)):
            os.makedirs(Dir)
        Serialize.WriteFile(aPath, aData)

    def Clear(self, aAge: int = 0):
        if (os.path.isdir(self.Root)):
            for x in DirWalk(self.Root, aType = 'f'):
                if (aAge):
                    if (time.time() - os.path.getmtime(x[0]) > aAge):
                        os.remove(x[0])
                else:
                    os.remove(x[0])

    def GetSize(self) -> int:
        if (os.path.isdir(self.Root)):
            Arr = [1 for _x in DirWalk(self.Root, aType = 'f')]
            Res = len(Arr)
        else:
            Res = 0
        return Res


class TCacheMem(TCache):
    Data = {}

    def _Get(self, aPath: str) -> str:
        Data = self.Data.get(aPath)
        if (Data) and (time.time() - Data[1] < self.MaxAge):
            return Data[0]

    def _Set(self, aPath: str, aData: str):
        self.Data[aPath] = (aData, time.time())

    def Clear(self, aAge: int = 0):
        if (aAge):
            Now = time.time()
            Keys = list(self.Data.keys())
            for xKey in Keys:
                _Data, Time = self.Data[xKey]
                if (Now - Time > aAge):
                    del self.Data[xKey]
        else:
            self.Data.clear()

    def GetSize(self):
        return len(self.Data)


class TCacheFileManager():
    def __init__(self, aRoot: str):
        self.Root = aRoot
        self.Data = {}

    def Clear(self):
        if (os.path.isdir(self.Root)):
            for x in DirWalk(self.Root, aType = 'f'):
                os.remove(x[0])

    def Init(self, aMaxAge: int) -> TCacheFile:
        if (aMaxAge not in self.Data):
            self.Data[aMaxAge] = TCacheFile(self.Root, aMaxAge)
        return self.Data[aMaxAge]

    async def Exec(self, aCache: TCacheFile, aFunc: callable, aFuncArgs: list, aRoute: str, aData: dict):
        return await aCache.ProxyA(aRoute, aData, aFunc, aFuncArgs)
