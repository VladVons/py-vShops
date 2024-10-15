# Created: 2024.09.27
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
from bs4 import BeautifulSoup
#
from Inc.Var.Dict import FilterNotNone
from .Utils import GetPrice


class TProductItemProp():
    def __init__(self, aSoup: BeautifulSoup):
        self.Root = aSoup
        self.Soup = aSoup.find_all(itemtype=re.compile('://schema.org/Product'))

    def Parse(self, aMaxCnt: int = 99) -> list:
        Res = []
        if (self.Soup):
            for Idx, xSoup in enumerate(self.Soup):
                if (Idx > aMaxCnt):
                    break

                R = {
                    'mpn': self.Mpn(xSoup),
                    'brand': self.Brand(xSoup),
                    'name': self.Name(xSoup),
                    'images': self.Images(xSoup),
                    'stock': self.Stock(xSoup),
                    'price': self.Price(xSoup),
                    'category': self.Category(xSoup),
                    'features': self.Features(xSoup)
                }

                if (R['images']) and (len(R['images']) == 1):
                    R['image'] = R['images'][0]
                    del R['images']
                R = FilterNotNone(R)
                Res.append(R)
            return Res

    @staticmethod
    def Mpn(aSoup: BeautifulSoup) -> str:
        Soup = aSoup.find(itemprop='mpn')
        if (Soup):
            return Soup.get('content')

    @staticmethod
    def Brand(aSoup: BeautifulSoup) -> str:
        Soup = aSoup.find(itemprop='brand')
        if (Soup):
            Res = Soup.get('content')
            if (not Res):
                Soup = Soup.find(itemprop='name')
                if (Soup):
                    Res = Soup.get('content')
            return Res


    @staticmethod
    def Name(aSoup: BeautifulSoup) -> str:
        Soup = aSoup.find('h1', itemprop='name')
        if (Soup):
            Res = Soup.text.strip()
        else:
            # try to exclude name in features. stupid schema.org
            Items = [
                tag for tag in aSoup.find_all(itemprop='name')
                if not tag.find_parent(itemprop=lambda x: x in ['additionalProperty', 'itemListElement'])
            ]

            if (Items):
                Res = Items[0].get('content')
                if (not Res):
                    Res = Items[0].text.strip()
                #Val = ''.join([char for char in Val if (char.isalpha() or char.isspace() or char.isdigit())])
        return Res

    @staticmethod
    def Images(aSoup: BeautifulSoup) -> list:
        Res = []
        Soup = aSoup.find_all(itemprop='image')
        if (Soup):
            for xSoup in Soup:
                if (xSoup.get('href')):
                    Val = xSoup.get('href')

                elif (xSoup.get('src')):
                    Val = xSoup.get('src')
                Res.append(Val)

        Soup = aSoup.find(itemtype=re.compile('://schema.org/ImageGallery'))
        # if (not Soup):
        #     Soup = self.Root.find(itemtype=re.compile('://schema.org/ImageGallery'))

        if (Soup):
            Soup = Soup.find_all(itemtype=re.compile('://schema.org/ImageObject'))
            for xSoup in Soup:
                Data = xSoup.find(itemprop='contentUrl')
                Val = Data.get('href')
                Res.append(Val)

        if (Res):
            return list(set(Res))

    @staticmethod
    def Stock(aSoup: BeautifulSoup) -> bool:
        Soup = aSoup.find(itemprop='offers')
        if (Soup):
            Data = Soup.find(itemprop='availability')
            if (Data):
                if (Data.get('href')):
                    Val = Data.get('href')
                elif (Data.get('content')):
                    Val = Data.get('content')
                else:
                    Val = ''
                return 'InStock' in Val

    @staticmethod
    def Price(aSoup: BeautifulSoup) -> list:
        Soup = aSoup.find(itemprop='offers')
        if (Soup):
            Data = Soup.find(itemprop='price')
            if (Data):
                Val = Data.get('content')
                if (not Val):
                    Val = Data.text.strip()

                Res = None
                try:
                    Res = [
                        float(Val),
                        Soup.find(itemprop='priceCurrency').get('content')
                    ]
                except ValueError:
                    Res = GetPrice(Val)
                return Res

    @staticmethod
    def Features(aSoup: BeautifulSoup) -> dict:
        Soup = aSoup.find_all(itemtype=re.compile('://schema.org/PropertyValue'))
        if (Soup):
            Res = {}
            for xProperty in Soup:
                Key = Val = None

                Soup2 = xProperty.find(itemprop='name')
                if (Soup2):
                    Key = Soup2.get('content')
                    if (not Key):
                        Key = Soup2.text.strip()

                Soup2 = xProperty.find(itemprop='value')
                if (Soup2):
                    Val = Soup2.get('content')
                    if (not Val):
                        Val = Soup2.text.strip()

                if (Key and Val):
                    Res[Key] = Val
            return Res

    @staticmethod
    def Category(aSoup: BeautifulSoup) -> str:
        Soup = aSoup.find(itemprop='category')
        if (Soup):
            Val = Soup.get('content')
            if (Val):
                return Val.strip()
        else:
            Soup = aSoup.find(itemtype=re.compile('://schema.org/BreadcrumbList'))
            if (Soup):
                ListLI = Soup.find_all(itemtype=re.compile('://schema.org/ListItem'))
                if (ListLI):
                    Res = []
                    for xListLI in ListLI:
                        Val = xListLI.find(itemprop='name')
                        if (Val):
                            Res.append(Val.text.strip())
                    return '/'.join(Res)
