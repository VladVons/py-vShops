# Created: 2022.04.11
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import json
import random
#
from Inc.DbList import TDbListSafe


#--- json ---
class TJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if (isinstance(o, TDbListSafe)):
            Res = o.Export()
        elif (isinstance(o, set)):
            Res = list(o)
        else:
            Res = str(o)
        return Res

    @staticmethod
    def Dumps(aObj):
        return json.dumps(aObj, cls = TJsonEncoder)

def FormatJsonStr(aScript: str, aPad: int = 2, aChar: str = ' ') -> str:
    Res = []
    Level = 0
    Lines = aScript.splitlines()
    for Line in Lines:
        Line = Line.strip()
        if (Line):
            if (Line[-1] in ['{', '[']):
                Spaces = Level * aPad
                Level += 1
            elif (Line[0] in ['}', ']']):
                Level -= 1
                Spaces = Level * aPad
            else:
                Spaces = Level * aPad
            Res.append((aChar * Spaces) + Line)
    return '\n'.join(Res)


#--- dict ---
def FilterKey(aData: object, aKeys: list, aInstance: list) -> object:
    def _FilterKey(aData: object, aKeys: list, aRes: dict, aPath: str):
        if (isinstance(aData, dict)):
            for Key, Val in aData.items():
                Path = (aPath + '.' + Key).lstrip('.')
                _FilterKey(Val, aKeys, aRes, Path)
                if (Key in aKeys):
                    if (aInstance == dict):
                        aRes[Path] = Val
                    elif (aInstance == list):
                        aRes.append(Val)
    if (aInstance not in [list, dict]):
        raise ValueError('Must be dict or list')

    Res = aInstance()
    _FilterKey(aData, aKeys, Res, '')
    return Res

def FilterKeyErr(aData: dict, aAsStr: bool = False) -> list:
    def _FilterKey(aData: object, aRes: list):
        if (isinstance(aData, dict)):
            for Key, Val in aData.items():
                _FilterKey(Val, aRes)
                if (Key == 'type') and (Val == 'err'):
                    aRes.append(aData.get('data'))
                elif (Key == 'err'):
                    aRes.append(aData.get('err'))

    Res = []
    _FilterKey(aData, Res)
    if (aAsStr):
        Res = ', '.join([str(x) for x in Res])
    return Res

def FilterNone(aData: dict, aTrue: bool) -> dict:
    return {
        Key: Val
        for Key, Val in aData.items()
        if ((Val is None) == aTrue)
    }

def FilterMatch(aData: dict, aFind: dict) -> int:
    Items = aData.items()
    return {
        Pair[0]: Pair[1]
        for Pair in aFind.items()
        if (Pair in Items)
    }


#--- string ---
def GetLeadCharCnt(aValue: str, aChar: str) -> int:
    return len(aValue) - len(aValue.lstrip(aChar))

def GetRandStr(aLen: int) -> str:
    def Range(aStart: int, aEnd: int) -> list:
        return [chr(i) for i in range(aStart,  aEnd)]

    Pattern = Range(48, 57) + Range(65, 90) + Range(97, 122)
    Rand = random.sample(Pattern, aLen)
    return ''.join(Rand)

def GetRandStrPattern(aLen: int, aPattern = 'YourPattern') -> str:
    return ''.join((random.choice(aPattern)) for x in range(aLen))


#--- misc
def GetEnvWithWarn(aName: str, aLog) -> object:
    Res = os.getenv(aName)
    if (Res is None):
        aLog.Print(1, 'e', f'Warn! environment variable {aName} is empty')
    return Res
