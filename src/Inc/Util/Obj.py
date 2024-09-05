# Created: 2020.02.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import re
import os
import sys
import json
#


def GetTree(aObj, aMaxDepth: int = 99) -> iter:
    '''
        Recursively walks through aObj and returns list of values:
        [Nested, Path, Obj, Depth]
    '''

    def Recurs(aObj, aPrefix: str, aDepth: int):
        if (aDepth < aMaxDepth):
            Type = type(aObj)
            if (Type == dict):
                yield (True, aPrefix, aObj, aDepth)
                for Key in aObj:
                    yield from Recurs(aObj[Key], aPrefix + '/' + Key, aDepth + 1)
            elif (Type in (list, tuple, set)):
                yield (True, aPrefix, aObj, aDepth)
                for Obj in aObj:
                    yield from Recurs(Obj, aPrefix, aDepth + 1)
            elif (Type in (str, int, float, bool)):
                yield (False, aPrefix, aObj, aDepth)
            elif (Type.__name__ in ['method', 'function']):
                yield (False, f'{aPrefix}()', aObj, aDepth)
            else:
                ClassName = aPrefix + '/' + aObj.__class__.__name__
                # if (Types.IsClass(aObj)):
                #     ClassName += '()'
                yield (True, ClassName, aObj, aDepth)
                for Key in dir(aObj):
                    if (not Key.startswith('_')):
                        Obj = getattr(aObj, Key)
                        yield from Recurs(Obj, ClassName + '/' + Key, aDepth + 1)
    yield from Recurs(aObj, '', 0)

def GetClassPath(aClass):
    def GetClassPathRecurs(aInstance: object, aPath: str = '', aDepth: int = 99) -> str:
        Instance = aInstance.__bases__
        if ( (Instance) and (aDepth > 0) ):
            aPath = GetClassPathRecurs(Instance[0], aPath, aDepth - 1)
        return aPath + '/' + aInstance.__name__

    return GetClassPathRecurs(aClass.__class__)

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

def DictUpdateDeep(aMaster: dict, aSlave: dict, aJoin = False, aDepth: int = 99) -> object:
    '''
    DictJoin({3: [1, 2, 3]}, {3: [4]}) -> {3: [1, 2, 3, 4]}
    '''
    def ParseEnv(aVal) -> object:
        if (isinstance(aVal, str)) and (aVal.startswith('{%')):
            Macro = re.findall(r'''\{%\s*(\w+)\s*([\w/.:-~]+)\s*%\}''', aVal)
            if (Macro):
                Type, Val = Macro[0]
                if (Type == 'env'):
                    aVal = os.getenv(Val, f'-{Val}-')
                elif (Type == 'file'):
                    File, *Path = Val.split(':')
                    with open(File, 'r', encoding = 'utf8') as F:
                        aVal = json.load(F)

                    if (Path):
                        aVal = DeepGet(aVal, Path[0])
                elif (Type == 'arg'):
                    if (Val in sys.argv):
                        Idx = sys.argv.index(Val)
                        aVal = sys.argv[Idx + 1]
                else:
                    raise ValueError()
        return aVal

    if (aDepth <= 0):
        return

    Type = type(aSlave)
    if (Type == dict):
        if (aMaster is None):
            aMaster = {}
        Res = aMaster

        for Key, Val in aSlave.items():
            Val = ParseEnv(Val)
            Tmp = aMaster.get(Key)
            if (Tmp is None):
                Tmp = {} if isinstance(Val, dict) else []
            Data = DictUpdateDeep(Tmp, Val, aJoin, aDepth - 1)
            Res[Key] = Data
    elif (Type == list):
        Res = [] if (aMaster is None ) else aMaster
        for Val in aSlave:
            Val = ParseEnv(Val)
            Data = DictUpdateDeep(None, Val, aJoin, aDepth - 1)
            if (aJoin):
                Res.append(Data)
            else:
                Res = Data
    else:
        Res = aSlave
    return Res

# more complex https://jmespath.org/examples.html
# Data = {'table': {'ref_product': {'foreign_key': {'tenant_id': {'table': 'x'}}}}}
# DeepGetRe(Data, ['^table', '.*_lang', '.*', '.*_id$', '.*'])
def DeepGetsRe(aObj, aKeys: list, aWithPath: bool = True) -> list:
    RegExSign = '.*+^$[({'

    def Recurs(aObj, aKeys: list, aPath: str) -> list:
        Res = []
        if (aKeys):
            Type = type(aObj)
            if (Type == dict):
                Key = aKeys[0]
                if (any(x in RegExSign for x in Key)):
                    for xKey in aObj:
                        if (re.match(Key, xKey)):
                            Res += Recurs(aObj.get(xKey), aKeys[1:], f'{aPath}.{xKey}')
                else:
                    Val = aObj.get(Key)
                    if (Val is not None):
                        Res += Recurs(Val, aKeys[1:], f'{aPath}.{Key}')
            elif (Type in [list, tuple, set]):
                for Idx, Val in enumerate(aObj):
                    Res += Recurs(Val, aKeys, f'{aPath}[{Idx}]')
        else:
            if (aWithPath):
                Res.append((aObj, aPath.lstrip('.')))
            else:
                Res.append(aObj)
        return Res
    return Recurs(aObj, aKeys, '')

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

def Iif(aCond: bool, aVal1, aVal2) -> object:
    return aVal1 if (aCond) else aVal2

def IifNone(aVal, aDef) -> object:
    return aDef if (aVal is None) else aVal

def IsDigits(aList: list) -> bool:
    return all(str(x).isdigit() for x in aList)
