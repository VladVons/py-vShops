# Created: 2023.01.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
import json
from bs4 import BeautifulSoup


StrWhiteSpacesEx = '\v\f\xA0✓→'
StrWhiteSpaces = ' \t\n\r' + StrWhiteSpacesEx
StrDigits = '0123456789'
StrDigitsDot = StrDigits + '.'
StrDigitsDotComma = StrDigits + '.,'
#_XlatEntitles = [('&nbsp;', ' '), ('&lt;', '<'), ('&amp;', '&'), ('&quot;', '"'), ('&apos;', "'")]
#
#ReCmp_Strip = re.compile(r'^\s+|\s+$')
ReCmp_Serial = re.compile(r'[A-Z0-9\-/]{5,}')


def DigDelThousands(aVal: str) -> str:
    Pos = aVal.rfind('.')
    if (len(aVal) - Pos - 1 == 3):
        aVal = aVal.replace('.', '')
    return aVal

def DigSplit(aVal: str) -> tuple:
    Digit = ''
    Before = ''
    After = ''
    WhiteSpaces = StrWhiteSpaces + "'"
    for x in aVal.rstrip('.'):
        if (x in WhiteSpaces):
            continue

        if (After == '') and (x in StrDigitsDotComma):
            if (x == ','):
                x = '.'
            Digit += x
        else:
            if (Digit):
                After += x
            else:
                Before += x
    Dots = Digit.count('.')
    if (Dots > 1):
        Digit = Digit.replace('.', '', Dots - 1)
    return (Before, DigDelThousands(Digit), After)

def SoupGetParents(aSoup: BeautifulSoup, aItems: list, aDepth: int = 99) -> list:
    Res = []
    for Item in aItems:
        Depth = aDepth
        ResLoop = []
        while (Item) and (Item != aSoup) and (Depth > 0):
            Attr = getattr(Item, 'attrs', None)
            if (Attr):
                ResLoop.append([Item.name, Attr])
            elif (Item.name):
                ResLoop.append([Item.name, {}])
            else:
                if (type(Item).__name__ == 'script'):
                    break
                ResLoop.append([Item, {}])
            Depth -= 1

            Item = Item.parent
        Res.append(ResLoop)
    return Res

def SoupGetParentsObj(aSoup: BeautifulSoup, aItems: list, aDepth: int = 99) -> BeautifulSoup:
    Res = []
    ResLoop = []
    for Item in aItems:
        Depth = aDepth
        while (Item) and (Item != aSoup) and (Depth > 0):
            ResLoop.append(Item)
            Item = Item.parent
            Depth -= 1
        Res.append(ResLoop)
    return Res


def SoupFindParents(aSoup: BeautifulSoup, aSearch: str) -> list:
    #Items = aSoup.findAll(string=aSearch)
    Items = aSoup.findAll(string=re.compile(aSearch))
    return SoupGetParents(aSoup, Items)

# https://www.scaler.com/topics/javascript/json-validator/
def GetLdJson(aSoup: BeautifulSoup) -> dict:
    def DelLastBrace(aPair: str):
        nonlocal Data

        Opened = Data.count(aPair[0])
        Closed = Data.count(aPair[1])
        if (Closed > Opened):
            LastBrace = Data.rfind(aPair[1])
            Data = Data[:LastBrace]

    Data: str = aSoup.text.strip()
    try:
        Res = json.loads(Data, strict=False)
    except json.JSONDecodeError as E:
        print('Exception:', E)

        Data = re.sub(r'\\(?!")', ' ', Data)

        # Replace = ' ' * len(StrWhiteSpacesEx)
        # Trans = str.maketrans(StrWhiteSpacesEx, Replace)
        # Data = Data.translate(Trans)

        # check for extra closes brace
        DelLastBrace('{}')
        DelLastBrace('[]')

        Res = json.loads(Data, strict=False)
    return Res
