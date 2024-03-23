# Created: 2023.06.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


def CryptSimple(aText: str, aKey: int) -> str:
    '''
    aText: string to crypt
    aKey: positive value to crypt, negativ value to uncrypt
    '''

    def _Shift(aVal: str, aKey: int) -> str:
        aKey %= len(aVal)
        return aVal[aKey:] + aVal[:aKey]


    LenText = len(aText)
    if (LenText == 0):
        return ''

    aKey = aKey + LenText if (aKey > 0) else aKey - LenText
    LenNum = ord('9') - ord('0') + 1
    LenLat = ord('z') - ord('a') + 1
    LenCyr = ord('я') - ord('а') + 1

    Arr = []
    for x in aText:
        if ('0' <= x <= '9'):
            Base = ord('0')
            Len = LenNum
        elif ('a' <= x <= 'z'):
            Base = ord('a')
            Len = LenLat
        elif ('A' <= x <= 'Z'):
            Base = ord('A')
            Len = LenLat
        elif ('а' <= x <= 'я'):
            Base = ord('а')
            Len = LenCyr
        elif ('А' <= x <= 'Я'):
            Base = ord('А')
            Len = LenCyr
        else:
            Arr.append(x)
            continue

        x = chr((ord(x) - Base + aKey) % Len + Base)
        Arr.append(x)

    Res = ''.join(Arr)
    return _Shift(Res, LenText * 3)

def GetCRC(aValue: str, aShift: int = 7) -> int:
    Res = 0
    for Char in aValue:
        Res ^= ord(Char) + aShift
        Res = (Res << 1) | (Res >> 31)
    ShiftCycleRight = ((Res >> aShift) | (Res << (32 - aShift))) & 0xFFFFFFFF
    return ShiftCycleRight
