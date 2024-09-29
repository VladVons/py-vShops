# Created: 2024.09.27
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
from bs4 import BeautifulSoup
#
from Inc.Var.Dict import DictUpdate
from .ProductItemProp import TProductItemProp
from .ProductLdJson import TProductLdJson


class TProduct():
    def __init__(self, aSoup: BeautifulSoup):
        self.Soup = aSoup

    def _TryImages(self, aSoup: BeautifulSoup):
        Pattern = r'(gallery-thumbs)'
        Soup = aSoup.find_all('div', class_=re.compile(Pattern))
        if (Soup):
            Res = []
            for xSoup in Soup:
                for xA in xSoup.find_all('a'):
                    Val = xA.get('href')
                    if (Val) and ('jpg' in Val):
                        Res.append(Val)

            if (Res):
                return {'images': Res}

    def _TryTableFeatures(self, aSoup: BeautifulSoup):
        def _FindBigTable():
            Max = [0, 0]
            for Idx, xTable in enumerate(Tables):
                FTr = xTable.find_all('tr')
                Len = len(FTr)
                if (Len >= Max[1]):
                    Max = [Idx, Len]
            return Max[0]

        Pattern = r'(features|product-feature|product-info|product-attributes)'
        Tables = aSoup.find_all('table', class_=re.compile(Pattern))
        if (Tables):
            Tr = []
            for xTable in Tables:
                for Row in xTable.find_all('tr'):
                    ResTag = []
                    Td = Row.find_all(['th', 'td'])
                    for xTd in Td:
                        Text = xTd.text.strip()
                        ResTag.append(Text)
                    Tr.append(ResTag)

            Res = {}
            for xTr in Tr:
                if (len(xTr) == 2):
                    Res[xTr[0]] = xTr[1]
            return {'features': Res}

    def _TryDivFeatures(self, aSoup):
        Pattern = r'(features)'
        Divs = aSoup.find_all('div', class_=re.compile(Pattern)) + aSoup.find_all('div', id=re.compile(Pattern))
        if (not Divs):
            return

    def Parse(self):
        Res = TProductLdJson(self.Soup).Parse()

        ItemProp = TProductItemProp(self.Soup)
        Res2 = ItemProp.Parse()
        DictUpdate(Res, Res2)

        if (ItemProp.Soup):
            Images = Res.get('images', [])
            if (len(Images) < 2):
                R = self._TryImages(ItemProp.Soup)

            if ('features' not in Res):
                self._TryTableFeatures(ItemProp.Soup)
                if ('features' not in Res):
                    self._TryDivFeatures(ItemProp.Soup)

        return Res
