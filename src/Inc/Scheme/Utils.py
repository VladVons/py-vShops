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

def GetPrice(aVal: str) -> list:
    Before, Dig, After = DigSplit(aVal)
    if (not Dig):
        Dig = '0'

    if (not After) and (Before):
        After = Before

    Res = [float(Dig), After.lower()]
    if (Res[0] > 0):
        return Res

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

def SoupTextTag(aSoup: BeautifulSoup, aTag: str = 'p') -> str:
    Arr = [xTag.get_text(strip=True, separator='\n') for xTag in aSoup.find_all(aTag)]
    if (Arr):
        Res = '\n'.join(Arr)
        return Res.strip()

def FindLineInScheme(aJson: str, aPath: str) -> int:
    # aPath = "/product/pipe_product/find/as_dict/features/find/table"

    def FindLineNo(aPattern: str, aStartLine: int) -> int:
        nonlocal Lines
        reKey = re.compile(aPattern)
        for i in range(aStartLine, len(Lines)):
            if reKey.search(Lines[i]):
                return i + 1
        return -1

    def Parse(aData, aKeys: iter) -> int:
        CurLine = 0
        for xKey in aKeys:
            if (isinstance(aData, dict)):
                if (xKey not in aData):
                    return

                CurLine = FindLineNo(rf'"{xKey}"\s*:', CurLine)
                if (CurLine < 0):
                    return

                aData = aData[xKey]
            elif (isinstance(aData, list)):
                for xData in aData:
                    if (xKey != xData[0]):
                        return

                    CurLine = FindLineNo(rf'[\s*"{xKey}"\s*]', CurLine)
                    if (CurLine < 0):
                        return

                    if (xKey == 'as_dict'):
                        aData = xData[1]
                        break

                    xKey = next(aKeys, None)
                    if (xKey is None):
                        break
        return CurLine

    try:
        Json = json.loads(aJson)
    except json.JSONDecodeError:
        return

    Lines = aJson.splitlines()
    Keys = aPath.lstrip('/').split('/')
    return Parse(Json, iter(Keys))
