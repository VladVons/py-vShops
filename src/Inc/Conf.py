# Created: 2018.06.10
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import sys
#
from .Util.FS import FileExists
from .DictDef import TDictDef


def ImportMod(aFile: str, aMod: list = None):
    if (aMod is None):
        aMod = ['*']

    #aMod = ['Main']
    #__import__(aPath)
    #Mod = sys.modules.get(aPath)
    return __import__(aFile.replace('/', '.'), None, None, aMod)


class TConf(TDictDef):
    def __init__(self, aFile: str):
        super().__init__()
        self.File = aFile

    def Load(self):
        Name, Ext = self.File.split('.')
        for Item in [Name, Name + '_' + sys.platform]:
            File = Item + '.' + Ext
            if (FileExists(File)):
                self._Load(File)

    def _Load(self, aFile: str):
        Name, *_ = aFile.split('.')
        Obj = ImportMod(Name)
        Keys = [x for x in dir(Obj) if (not x.startswith('__'))]
        for Key in Keys:
            self[Key] = getattr(Obj, Key, None)

    def Save(self):
        with open(self.File, 'w', encoding = 'utf-8') as File:
            for K, V in sorted(self.items()):
                if (isinstance(V, str)):
                    V = f"'{V}'"
                File.write(f'{K} = {V}\n')
