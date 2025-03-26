# Created: 2020.02.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
import random
import json
import base64


def SplitPad(aCnt: int, aVal: str, aDelim: str) -> list:
    R = aVal.split(aDelim, aCnt - 1)
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

def ToInt(aVal: str, aDef: int = 0) -> int:
    if (not aVal):
        aVal = aDef
    else:
        if (isinstance(aVal, float)):
            aVal = int(aVal)
        elif (isinstance(aVal, str)):
            if (aVal.isdigit()):
                aVal = int(aVal)
            else:
                aVal = aDef
    return aVal

def ToBool(aVal: str) -> bool:
    return aVal.lower() in ('true', '1', 'yes', 'y', 't')

# https://www.scaler.com/topics/javascript/json-validator/
def ToJson(aVal: str) -> dict:
    def DelLastBrace(aPair: str):
        nonlocal Data

        Opened = Data.count(aPair[0])
        Closed = Data.count(aPair[1])
        if (Closed > Opened):
            LastBrace = Data.rfind(aPair[1])
            Data = Data[:LastBrace]

    try:
        Res = json.loads(aVal, strict=False)
    except json.JSONDecodeError as E:
        print('Exception:', E)

        Data = re.sub(r'\\(?!")', ' ', aVal)

        # "Laptopy 14"" -> "Laptopy 14\""
        if ('""' in Data):
            Data = re.sub(r'(\d)""', r'\1\\""', Data)

        # "from 13" to" -> "from 13\" to"
        Data = re.sub(r'(\d)" ', r'\1\\"', Data)

        # ""Dell"" -> "Dell"
        Data = re.sub(r'""(.*?)""', r'"\1"', Data)

        # Replace = ' ' * len(StrWhiteSpacesEx)
        # Trans = str.maketrans(StrWhiteSpacesEx, Replace)
        # Data = Data.translate(Trans)

        # check for extra closes brace
        DelLastBrace('{}')
        DelLastBrace('[]')

        Res = json.loads(Data, strict=False)
    return Res

def JsonFormat(aScript: str, aPad: int = 2, aChar: str = ' ') -> str:
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

def JsonKeyPos(aScript: str, aKey: str, aBrackets = '{}') -> list[int]:
    #python has no recursive re
    #reInfo = re.compile(r'"info":\s*{[^}]*}', flags=re.DOTALL) #ToDo
    Res = []
    Level = 0
    Lines = aScript.splitlines()
    for Idx, Line in enumerate(Lines):
        Line = Line.strip()
        if (Line):
            if (f'"{aKey}"' in Line) and (Line[-1] == aBrackets[0]):
                Level += 1
                Res.append(Idx+1)
            elif (Level > 0):
                if (Line[-1] == aBrackets[0]):
                    Level += 1
                elif (Line[0] == aBrackets[-1]):
                    Level -= 1
                    if (Level == 0):
                        Res.append(Idx-1)
                        return Res

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


def ToHashHex(aVal: str) -> str:
    return hex(abs(hash(aVal)))

def ToHashW(aVal: str) -> str:
    Res = re.sub(r'[\s/]+', ' ', aVal)
    Res = re.sub(r'[^a-zA-Z0-9\s]', '', Res)
    Res = Res.lower()
    #Res = re.sub(r'[^\w]', '', Res).lower()
    #Res = ''.join(sorted(list(Res)))
    #Res = hex(hash(Res) & 0xFFFFFFFFFFFFFFFF)[2:]
    return Res

def ToHashWM(aVal: str) -> str:
    Res = re.sub(r'[\s/]+', ' ', aVal)
    Res = re.sub(r'[^a-zA-Z0-9\s-]', '', Res)
    Res = Res.lower().rstrip('-')
    return Res

def Replace(aVal: str, aReplace: dict) -> str:
    if (aVal):
        for Old, New in aReplace.items():
            aVal = aVal.replace(Old, New)
    return aVal

def ConcatUniq(aVal: str, aAdd: list[str]) -> str:
    for xAdd in aAdd:
        if (xAdd not in aVal):
            aVal += xAdd
    return aVal

def StartsWith(aVal: str, aItems: list[str]) -> str:
    for xItem in aItems:
        if (aVal.startswith(xItem)):
            return xItem

def GetLeadCharCnt(aVal: str, aChar: str) -> int:
    return len(aVal) - len(aVal.lstrip(aChar))

def GetRandStr(aLen: int) -> str:
    def Range(aStart: int, aEnd: int) -> list:
        return [chr(i) for i in range(aStart,  aEnd)]

    Pattern = Range(48, 57) + Range(65, 90) + Range(97, 122)
    Rand = random.sample(Pattern, aLen)
    return ''.join(Rand)

def GetRandStrPattern(aLen: int, aPattern = 'YourPattern') -> str:
    return ''.join((random.choice(aPattern)) for x in range(aLen))

def EncryptXor(aVal: str, aKey: str = 'K'):
    Xor = (chr(ord(x) ^ ord(aKey)) for x in aVal)
    return base64.urlsafe_b64encode(''.join(Xor).encode()).decode()

def DecryptXor(aVal: str, aKey: str = 'K'):
    Str = base64.urlsafe_b64decode(aVal.encode()).decode()
    Arr = (chr(ord(x) ^ ord(aKey)) for x in Str)
    return ''.join(Arr)
