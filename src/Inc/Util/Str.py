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

def ConcatUniq(aText: str, aAdd: list[str]) -> str:
    for xAdd in aAdd:
        if (xAdd not in aText):
            aText += xAdd
    return aText

def CyrToLat(aText: str) -> str:
    Cyr = ['а', 'б', 'в', 'г', 'ґ', 'д', 'е', 'є',  'ж',  'з', 'и', 'і', 'ї',  'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х',  'ц',  'ч',  'ш',  'щ',    'ю',  'я', 'ь']
    Lat = ['a', 'b', 'v', 'h', 'g', 'd', 'e', 'ye', 'zh', 'z', 'y', 'i', 'yi', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f', 'kh', 'ts', 'ch', 'sh', 'shch', 'yu', 'ya', '']

    Res = []
    for x in aText:
        if ('а' < x <= 'ь'):
            Idx = Cyr.index(x)
            x = Lat[Idx]
        elif ('А' < x <= 'Ь'):
            Idx = Cyr.index(x.lower())
            x = Lat[Idx].capitalize()
        Res.append(x)
    return ''.join(Res)
