# Created: 2022.02.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Obj import DeepGetByList, DeepSetByList


class TDictDef(dict):
    def __init__(self, aDef: object = None, aData: dict = None):
        self.Def = aDef

        if (aData is None):
            aData = {}
        super().__init__(aData)

    def __getattr__(self, aName: str) -> object:
        return self.get(aName, self.Def)

    def Set(self, aName: str, aVal: object):
        if ('.' in aName):
            DeepSetByList(self, aName.split('.'), aVal)
        else:
            self[aName] = aVal

    def Get(self, aName: str, aDef = None) -> object:
        Def = self.Def if (aDef is None) else aDef
        if ('.' in aName):
            Res = DeepGetByList(self, aName.split('.'), Def)
        else:
            Res = self.get(aName, Def)
        return Res

    def SetData(self, aData: dict):
        super().__init__(aData)
