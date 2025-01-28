# Created: 2024.09.23
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import json

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

def DeepGetDef(aData: dict, aKeys: list, aDef: list) -> list:
    if (aData):
        Res = [DeepGetByList(aData, Key.split('.'), Def) for Key, Def in zip(aKeys, aDef)]
    else:
        Res = aDef
    return Res

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

def FilterNone(aData: dict, aTrue: bool) -> dict:
    return {
        Key: Val
        for Key, Val in aData.items()
        if ((Val is None) == aTrue)
    }

def DelValues(aData: dict, aVals: list):
    '''
    Recursively del values that match a list
    Del(dict1, ['', [], {}, None])
    '''
    Keys = list(aData.keys())
    for xKey in Keys:
        Val = aData[xKey]
        if (Val in aVals):
            del aData[xKey]
        elif (isinstance(Val, dict)):
            DelValues(Val, aVals)

def FilterMatch(aData: dict, aFind: dict) -> int:
    Items = aData.items()
    return {
        Pair[0]: Pair[1]
        for Pair in aFind.items()
        if (Pair in Items)
    }

def SetNotNone(aData: dict, aKey: str, aVal: object):
    if (aVal is not None):
        aData[aKey] = aVal

def Filter(aData: dict, aKeys: list) -> dict:
    return {Key: aData[Key] for Key in aKeys if (Key in aData)}

def GetDict(aData: dict, aKeys: list, aStrict: bool = False) -> list:
    if (aStrict):
        Res = [aData[x] for x in aKeys]
    else:
        Res = [aData.get(x) for x in aKeys]
    return Res

def DictFindVal(aData: dict, aVal: object, aDefKey: str) -> str:
    for xKey, xVal in aData.items():
        if (xVal == aVal):
            return xKey
    return aDefKey

def GetDictDef(aData: dict, aKeys: list, aDef: list) -> list:
    if (aData):
        Res = [aData.get(Key, Def) for Key, Def in zip(aKeys, aDef, strict=True)]
    else:
        Res = aDef
    return Res

def GetDictDefs(aData: dict, aKeys: list, aDef: list) -> list:
    def WGet(aKey, aDef) -> object:
        if (isinstance(aDef, tuple)):
            Res = aData.get(aKey)
            if (Res not in aDef):
                Res = aDef[0]
        else:
            try:
                Res = type(aDef)(aData.get(aKey, aDef))
            except Exception as _E:
                Res = aDef
        return Res

    if (aData):
        Res = [WGet(Key, Def) for Key, Def in zip(aKeys, aDef, strict=True)]
    else:
        Res = aDef
    return Res

def DictUpdate(aMaster: dict, aSlave: dict, aOverwrite: bool = True):
    if (isinstance(aSlave, dict)):
        if (aMaster == {}):
            aMaster.update(aSlave)
        else:
            for xKey, xVal in aSlave.items():
                if (xKey in aMaster):
                    if (aOverwrite):
                        if (isinstance(xVal, dict)):
                            aMaster[xKey].update(xVal)
                        elif (isinstance(xVal, list)):
                            aMaster[xKey].extend(xVal)
                        else:
                            aMaster[xKey] = xVal
                else:
                    aMaster[xKey] = xVal

def DictUpdateDef(aMaster: dict, aSlave: dict, aDef: object):
    if (isinstance(aSlave, dict)):
        if (aMaster == {}) or (aMaster.keys() == aSlave.keys()):
            aMaster.update(aSlave)
        else:
            for xKey in aMaster:
                aMaster[xKey] = aSlave.get(xKey, aDef)

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

def SortByValue(aData: dict, aName: str) -> list:
    # SortD({'a1': {'key': 1, 'val': 111}, 'a2':{'key': 2, 'val': 222}})
    return sorted(aData.items(), key = lambda k: k[1].get(aName))

def DictToPath(aObj) -> dict:
    def _Recurs(aObj, aPath: str, aRes: dict) -> dict:
        if (isinstance(aObj, dict)):
            for xKey, xVal in aObj.items():
                Path = f'{aPath}/{xKey}' if aPath else xKey
                _Recurs(xVal, Path, aRes)
        else:
            aRes[aPath] = aObj

    Res = {}
    _Recurs(aObj, '', Res)
    return Res


def ToHash(aData: dict) -> int:
    if (aData):
        Str = json.dumps(aData, sort_keys=True)
        Res = hash(Str) & 0x7FFFFFFF
    else:
        Res = 0
    return Res
