# Creatad: 2022.10.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import json
from Inc.Util.Obj import DeepGet, DictUpdateDeep
from Inc.Misc.FS import DirWalk


class TConfJson(dict):
    def Init(self, aData: dict):
        super().__init__(aData)

    def _ReadFile(self, aFile: str) -> dict:
        with open(aFile, 'r', encoding = 'utf-8') as F:
            return json.load(F)

    @staticmethod
    def _Join(aData: list) -> dict:
        Res = {}
        for xData in aData:
            if (xData):
                Data = DictUpdateDeep(Res, xData, True)
                Res.update(Data)
        return Res

    def GetKey(self, aPath: str, aDef = None) -> object:
        return DeepGet(self, aPath, aDef)

    def JoinKeys(self, aKey: list) -> dict:
        Data = [DeepGet(self, xKey, {}) for xKey in aKey]
        return self._Join(Data)

    def LoadDir(self, aDir: str, aJoin: bool = True):
        for xDir in DirWalk(aDir, '.json$', 'f', 0):
            self.LoadFile(xDir[0], aJoin)

    def LoadFile(self, aFile: str, aJoin: bool = True) -> dict:
        Data = self._ReadFile(aFile)
        if (aJoin):
            Data = self._Join([self, Data])
            self.Init(Data)
        else:
            self.update(Data)
        return dict(self)

    def LoadList(self, aPath: list[str], aJoin: bool = True, aCheck: bool = False) -> dict:
        for File in aPath:
            if os.path.exists(File):
                if (os.path.isdir(File)):
                    self.LoadDir(File)
                else:
                    self.LoadFile(File, aJoin)
            elif (aCheck):
                assert(False), f'File not exists {File}'
        return dict(self)
