# Created: 2024.09.23
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


def DeepGets(aObj, aKeys: list) -> list:
    Res = []
    if (aKeys):
        Type = type(aObj)
        if (Type == dict):
            Val = aObj.get(aKeys[0])
            if (Val is not None):
                Res += DeepGets(Val, aKeys[1:])
        elif (Type in [list, tuple, set]):
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

def Filter(aData: dict, aKeys: list) -> dict:
    return {Key: aData[Key] for Key in aKeys }

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

def DictUpdate(aMaster: dict, aSlave: dict):
    if (not aMaster):
        aMaster.update(aSlave)
    elif (aSlave):
        for Key, Val in aSlave.items():
            if (Key in aMaster):
                if (isinstance(Val, dict)):
                    aMaster[Key].update(Val)
                elif (isinstance(Val, list)):
                    aMaster[Key].extend(Val)
                else:
                    aMaster[Key] = Val
            else:
                aMaster[Key] = Val
