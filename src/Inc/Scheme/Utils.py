# Created: 2023.01.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
from bs4 import BeautifulSoup


StrWhiteSpaces = ' \t\n\r\v\f\xA0✓→'
StrDigits = '0123456789'
StrDigitsDot = StrDigits + '.'
StrDigitsDotComma = StrDigits + '.,'
#_XlatEntitles = [('&nbsp;', ' '), ('&lt;', '<'), ('&amp;', '&'), ('&quot;', '"'), ('&apos;', "'")]
#
#ReCmp_Strip = re.compile(r'^\s+|\s+$')
ReCmp_Serial = re.compile(r'[A-Z0-9\-/]{5,}')


class TInStock():
    _MatchYes = [
        # en
        'http://schema.org/instock',
        'https://schema.org/instock',
        'instock',

        # ua
        'в наявності на складі',
        'в наявності',
        'в кошик',
        'до кошика',
        'додати у кошик',
        'добавити в корзину',
        'є в наявності',
        'є у наявності',
        'є на складі',
        'закінчується',
        'купити',
        'на складі',
        'товар в наявності',
        'товар є в наявності',
        'склад',

        # ru
        'в корзину',
        'в наличии на складе',
        'в наличии',
        'добавить в корзину',
        'есть в наличии',
        'есть на складе',
        'есть',
        'заканчивается',
        'купить',
        'на складе',
        'товар в наличии',
        'товар есть в наличии',
    ]

    _MatchNo = [
        # ua
        'немає в наявності',

        # ru
        'нет в наличии'
    ]

    _Del = [
        ' шт.'
    ]

    def __init__(self):
        self.Trans = str.maketrans('', '', StrDigits)

    def Check(self, aVal: str, aMatch: bool) -> bool:
        aVal = aVal.translate(self.Trans).strip().lower()
        for Item in self._Del:
            aVal = aVal.replace(Item, '')
        Match = self._MatchYes if (aMatch) else self._MatchNo
        return aVal in Match

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
