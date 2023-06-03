# Created: 2023.06.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#


def SimpleCrypt(aText: str, aShift: int) -> str:
    '''
    aText: string to crypt
    aShift: positive valu to crypt. negativ value to uncrypt
    '''

    def _Shift(aVal: str, aShift: int) -> str:
        aShift %= len(aVal)
        return aVal[aShift:] + aVal[:aShift]

    Arr = []
    for x in aText:
        if ('a' <= x <= 'z'):
            x = chr((ord(x) - 97 + aShift) % 26 + 97)
        elif ('A' <= x <= 'Z'):
            x = chr((ord(x) - 65 + aShift) % 26 + 65)
        elif ('0' <= x <= '9'):
            x = str((int(x) + aShift) % 10)
        Arr.append(x)
    return _Shift(''.join(Arr), aShift * 2)
