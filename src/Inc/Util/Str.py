# Created: 2020.02.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re


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
