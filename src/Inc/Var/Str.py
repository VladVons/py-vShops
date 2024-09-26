# Created: 2020.02.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
import json

def SplitPad(aCnt: int, aStr: str, aDelim: str) -> list:
    R = aStr.split(aDelim, aCnt - 1)
    for _i in range(aCnt - len(R)):
        R.append('')
    return R

def ToFloat(aVal: str) -> float:
    if (not aVal):
        aVal = 0
    elif (isinstance(aVal, str)):
        aVal = aVal.replace(',', '.').replace(' ', '')

    try:
        aVal = float(aVal)
    except ValueError:
        aVal = 0.0
    return aVal

def ToInt(aVal: str) -> int:
    if (not aVal):
        aVal = 0
    else:
        aVal = int(aVal)
    return aVal

def ToBool(aVal: str) -> bool:
    return aVal.lower() in ('true', '1', 'yes', 'y', 't')

def ToObj(aVal: str) -> object:
    if (not isinstance(aVal, str)) or (aVal == ''):
        return aVal

    if (aVal.isdigit()):
        return int(aVal)

    Dots = aVal.count('.')
    if (Dots == 1):
        Left, Right = aVal.split('.')
        if (Left.isdigit() and Right.isdigit()):
            return float(aVal)

    ValL = aVal.lower().strip()

    if (ValL.startswith('[') and ValL.endswith(']')) or \
       (ValL.startswith('{') and ValL.endswith('}')):
        return json.loads(aVal)

    if (ValL in ('true', 'yes')):
        return True
    if (ValL in ('false', 'no')):
        return False

    return aVal


def ToHashW(aText: str) -> str:
    Res = re.sub(r'[\s/]+', ' ', aText)
    Res = re.sub(r'[^a-zA-Z0-9\s]', '', Res)
    Res = Res.lower()
    #Res = re.sub(r'[^\w]', '', Res).lower()
    #Res = ''.join(sorted(list(Res)))
    #Res = hex(hash(Res) & 0xFFFFFFFFFFFFFFFF)[2:]
    return Res

def ToHashWM(aText: str) -> str:
    Res = re.sub(r'[\s/]+', ' ', aText)
    Res = re.sub(r'[^a-zA-Z0-9\s-]', '', Res)
    Res = Res.lower().rstrip('-')
    return Res

def Replace(aText: str, aReplace: dict) -> str:
    if (aText):
        for Old, New in aReplace.items():
            aText = aText.replace(Old, New)
    return aText

def ConcatUniq(aText: str, aAdd: list[str]) -> str:
    for xAdd in aAdd:
        if (xAdd not in aText):
            aText += xAdd
    return aText

def StartsWith(aText: str, aItems: list[str]) -> str:
    for xItem in aItems:
        if (aText.startswith(xItem)):
            return xItem
