# Created: 2023.01.20
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import sys
#
from IncP.Log import Log


class TPlugin(dict):
    def __init__(self, aDirMod: str = '', aDirConf: str = ''):
        #assert (aDirMod and os.path.isdir(aDirMod)), f'Directory not exists {aDirMod}'
        super().__init__()

        self.Dir = aDirMod
        self.DirConf = aDirConf
        self.Cache = {}

    def _Create(self, _aModule: object, _aPath: str) -> object:
        raise NotImplementedError()

    def _GetPath(self, aPath: str) -> str:
        return f'{self.Dir}/{aPath}'

    def Find(self, aKey: str) -> list:
        return [Val[0] for Key, Val in self.items() if aKey in Key]

    def LoadMod(self, aPath: str, aRegister: bool = True) -> dict:
        Res = {}
        if (not aPath) or (aPath.startswith('-')) or (self.get(aPath)):
            return Res

        Path = self._GetPath(aPath).replace('/', '.')
        __import__(Path)
        Mod = sys.modules[Path]
        Enable = getattr(Mod, 'enable', True)
        if (Enable):
            Depends = getattr(Mod, 'depends', '')
            for xDepend in Depends.split():
                if (xDepend):
                    Log.Print(1, 'i', f'{aPath} depends on {xDepend}')
                    ResF = self.LoadMod(xDepend)
                    Res.update(ResF)
            Obj = self._Create(Mod, aPath)

            if (Obj):
                Method = getattr(Obj, '_init_', None)
                if (Method):
                    Method()

                if (aRegister):
                    self[aPath] = Obj
                Res[aPath] = Obj
        else:
            Log.Print(1, 'i', f'{aPath} disabled')
        return Res

    def LoadList(self, aPath: str, aSkip: str = ''):
        Skip = aSkip.split()
        for Path in aPath.split():
            if (Path not in Skip):
                self.LoadMod(Path)

    def LoadDir(self, aDir: str):
        assert (os.path.isdir(aDir)), f'Directory not exists {aDir}'

        Files = os.listdir(aDir)
        for Info in Files:
            if (Info[1] & 0x4000): # is dir
                DirName = Info[0]
                self.LoadMod(aDir.replace('/', '.') + '.' + DirName)
