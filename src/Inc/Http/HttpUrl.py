# Created: 2021.01.10
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re

# AI
reUrlSplit = re.compile(
    r'^(?P<scheme>https?|ftp)://'
    r'(?P<host>[^:/?#]+)'\
    r'(?:\:(?P<port>\d+))?'
    r'(?P<path>/[^?#]*)?'
    r'(?:\?(?P<query>[^#]*))?'
    r'(?:#(?P<fragment>.*))?$',
    flags=re.ASCII
)

def UrlPercent(aData: bytearray) -> str:
    Bits = aData.split(b'%')
    Arr = [Bits[0]]
    for Item in Bits[1:]:
        Code = Item[:2]
        Char = bytes([int(Code, 16)])
        Arr.append(Char)
        Arr.append(Item[2:].replace(b'+', b' '))
    Res = b''.join(Arr)
    return Res.decode('utf-8')

def UrlToDict(aUrl: str) -> dict:
    Match = reUrlSplit.match(aUrl)
    if (Match):
        return Match.groupdict()

def UrlToStr(aQuery: dict, aParts: list = None) -> str:
    Order = [
        ('', 'scheme', '://'),
        ('', 'host', ''),
        (':', 'port', ''),
        ('/', 'path', ''),
        ('?', 'query', ''),
        ('#', 'fragment', '')
    ]

    Arr = []
    for xStart, xName, xEnd in Order:
        Val = aQuery.get(xName)
        if (Val) and ((not aParts) or (xName in aParts)):
            Arr.append(f'{xStart}{Val.lstrip(xStart)}{xEnd}')
    return ''.join(Arr)

def UrlParseValidate(aUrl: str) -> list:
    # by cx 2023.03.20
    Pattern = r'^([a-z]{2,})://([a-z0-9]{1}[a-z0-9-.]*[a-z0-9]{1})[:]?(\d*)([/]?[a-zA-Z0-9-_.%]*)[?]?([a-zA-Z0-9-_.%=&]*)[#]?(.*)'
    return re.findall(Pattern, aUrl, flags=re.ASCII)

def QueryToDict(aQuery: str) -> dict:
    Res = {}
    for xParam in aQuery.split('&'):
        Pair = xParam.split('=', maxsplit=1)
        if (len(Pair) == 2):
            Res[Pair[0]] = Pair[1]
        else:
            Res[Pair[0]] = None
    return Res

def QueryToStr(aQuery: dict) -> str:
    Arr = []
    for xKey, xVal in aQuery.items():
        if (xVal is None):
            Arr.append(xKey)
        else:
            Arr.append(f'{xKey}={xVal}')
    return '='.join(Arr)
