# Creatad: 2022.10.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import json
from Inc.Util.Obj import DeepGet, DictUpdate
from Inc.Misc.FS import DirWalk


class TConfJson(dict):
    def Init(self, aData: dict):
        super().__init__(aData)

    def _ReadFile(self, aFile: str) -> dict:
        with open(aFile, 'r', encoding = 'utf-8') as F:
            return json.load(F)

    @staticmethod
    def _Join(aDict: list) -> dict:
        Res = {}
        for x in aDict:
            if (x):
                Data = DictUpdate(Res, x, True)
                Res.update(Data)
        return Res

    def GetKey(self, aPath: str, aDef = None) -> object:
        return DeepGet(self, aPath, aDef)

    def JoinKeys(self, aKey: list) -> dict:
        Data = [DeepGet(self, x, {}) for x in aKey]
        return self._Join(Data)

    def LoadDir(self, aDir: str, aJoin: bool = True):
        for x in DirWalk(aDir, '.json$', 'f', 0):
            self.LoadFile(x[0], aJoin)

    def LoadFile(self, aFile: str, aJoin: bool = True):
        Data = self._ReadFile(aFile)
        if (aJoin):
            Data = self._Join([self, Data])
            self.Init(Data)
        else:
            self.update(Data)

    def LoadList(self, aPath: list[str], aJoin: bool = True):
        for File in aPath:
            if os.path.exists(File):
                if (os.path.isdir(File)):
                    self.LoadDir(File)
                else:
                    self.LoadFile(File, aJoin)
