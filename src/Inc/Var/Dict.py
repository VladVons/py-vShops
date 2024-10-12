# Created: 2024.09.23
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


def DeepGets(aObj, aKeys: list) -> list:
    Res = []
    if (aKeys):
        if isinstance(aObj, dict):
            Val = aObj.get(aKeys[0])
            if (Val is not None):
                Res += DeepGets(Val, aKeys[1:])
        elif isinstance(aObj, (list, tuple, set)):
            for Val in aObj:
                Res += DeepGets(Val, aKeys)
    else:
        Res.append(aObj)
    return Res

def DeepGetByList(aData: dict, aKeys: list, aDef = None) -> object:
    for Key in aKeys:
        if (isinstance(aData, dict)) or (hasattr(aData, 'get')):
            aData = aData.get(Key)
            if (aData is None):
                return aDef
        else:
            return aDef
    return aData

def DeepGet(aData: dict, aDotKeys: str, aDef = None) -> object:
    return DeepGetByList(aData, aDotKeys.split('.'), aDef)

def DeepSetByList(aData: dict, aKeys: list, aValue: object) -> dict:
    for Key in aKeys[:-1]:
        if (Key):
            Data = aData.get(Key)
            if (Data is None):
                aData[Key] = Data = {}
            aData = Data
    aData[aKeys[-1]] = aValue
    return aData

def DeepSet(aData: dict, aDotKeys: str, aValue: object) -> dict:
    return DeepSetByList(aData, aDotKeys.split('.'), aValue)

def GetNotNone(aData: dict, aKey: str, aDef: object) -> object:
    Res = aData.get(aKey, aDef)
    if (Res is None):
        Res = aDef
    return Res

def SetNotNone(aData: dict, aKey: str, aVal: object):
    if (aVal is not None):
        aData[aKey] = aVal

def Filter(aData: dict, aKeys: list) -> dict:
    return {Key: aData[Key] for Key in aKeys if (Key in aData)}

def FilterNotNone(aData: dict) -> dict:
    return {Key: Val for Key, Val in aData.items() if (Val is not None)}

def GetDict(aData: dict, aKeys: list, aStrict: bool = False) -> list:
    if (aStrict):
        Res = [aData[x] for x in aKeys]
    else:
        Res = [aData.get(x) for x in aKeys]
    return Res

def GetDictDef(aData: dict, aKeys: list, aDef: list) -> list:
    if (aData):
        Res = [aData.get(Key, Def) for Key, Def in zip(aKeys, aDef, strict=True)]
    else:
        Res = aDef
    return Res

def GetDictDefs(aData: dict, aKeys: list, aDef: list) -> list:
    def _Get(aKey, aDef) -> object:
        if (isinstance(aDef, tuple)):
            Res = aData.get(aKey)
            if (Res not in aDef):
                Res = aDef[0]
        else:
            try:
                Res = type(aDef)(aData.get(aKey, aDef))
            except Exception as _E:
                Res = None
        return Res

    if (aData):
        Res = [_Get(Key, Def) for Key, Def in zip(aKeys, aDef, strict=True)]
    else:
        Res = aDef
    return Res

def GetDictDefDeep(aData: dict, aKeys: list, aDef: list) -> list:
    if (aData):
        Res = [DeepGetByList(aData, Key.split('.'), Def) for Key, Def in zip(aKeys, aDef)]
    else:
        Res = aDef
    return Res

def DictUpdate(aMaster: dict, aSlave: dict, aOverwrite: bool = True):
    if (not aMaster):
        aMaster.update(aSlave)
    elif (aSlave):
        for Key, Val in aSlave.items():
            if (Key in aMaster):
                if (aOverwrite):
                    if (isinstance(Val, dict)):
                        aMaster[Key].update(Val)
                    elif (isinstance(Val, list)):
                        aMaster[Key].extend(Val)
                    else:
                        aMaster[Key] = Val
            else:
                aMaster[Key] = Val

def DictToText(aData: dict, aDelim: str = '\n') -> str:
    Arr = [f'{Key}:{Val}' for Key, Val in aData.items()]
    return aDelim.join(Arr)

def DictDiff(aData1: dict, aData2: dict) -> dict:
    if (aData1 is None):
        aData1 = {}

    if (aData2 is None):
        aData2 = {}

    New = {Key: aData2[Key] for Key in aData2 if Key not in aData1}
    Del = {Key: aData1[Key] for Key in aData1 if Key not in aData2}
    Mod = {Key: (aData1[Key], aData2[Key]) for Key in aData1 if Key in aData2 and aData1[Key] != aData2[Key]}

    return {
        'new': New,
        'del': Del,
        'mod': Mod,
        'changed': bool(New) or bool(Del) or bool(Mod)
    }
