# Created: 2024.09.27
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
from bs4 import BeautifulSoup
#
from Inc.Var.Dict import FilterNotNone


class TProductItemProp():
    def __init__(self, aSoup: BeautifulSoup):
        self.Root = aSoup
        self.Soup = aSoup.find(itemtype=re.compile('://schema.org/Product'))

    def Parse(self) -> dict:
        if (self.Soup):
            Data = {
                'mpn': self.Mpn(),
                'brand': self.Brand(),
                'name': self.Name(),
                'images': self.Images(),
                'stock': self.Stock(),
                'price': self.Price(),
                'category': self.Category(),
                'features': self.Features()
            }

            if (len(Data['images']) == 1):
                Data['image'] = Data['images'][0]
                del Data['images']

            return FilterNotNone(Data)

    def Mpn(self) -> str:
        Soup = self.Soup.find(itemprop='mpn')
        if (Soup):
            return Soup.get('content')

    def Brand(self) -> str:
        Soup = self.Soup.find(itemprop='brand')
        if (Soup):
            return Soup.get('content')

    def Name(self) -> str:
        Items = [
            tag for tag in self.Soup.find_all(itemprop='name')
            if not tag.find_parent(itemprop='itemListElement')
        ]

        if (Items):
            Res = Items[0].get('content')
            if (not Res):
                Res = Items[0].text.strip()
                if (len(Res) < 10):
                    Soup = self.Soup.find('h1', itemprop='name')
                    if (Soup):
                        Res = Soup.text.strip()
            #Val = ''.join([char for char in Val if (char.isalpha() or char.isspace() or char.isdigit())])
            return Res

    def Images(self) -> list:
        Res = []
        Soup = self.Soup.find_all(itemprop='image')
        if (Soup):
            for xSoup in Soup:
                if (xSoup.get('href')):
                    Val = xSoup.get('href')

                elif (xSoup.get('src')):
                    Val = xSoup.get('src')
                Res.append(Val)

        Soup = self.Soup.find(itemtype=re.compile('://schema.org/ImageGallery'))
        if (not Soup):
            Soup = self.Root.find(itemtype=re.compile('://schema.org/ImageGallery'))

        if (Soup):
            Soup = Soup.find_all(itemtype=re.compile('://schema.org/ImageObject'))
            for xSoup in Soup:
                Data = xSoup.find(itemprop='contentUrl')
                Val = Data.get('href')
                Res.append(Val)

        if (Res):
            return list(set(Res))

    def Stock(self) -> bool:
        Soup = self.Soup.find(itemprop='offers')
        if (Soup):
            Data = Soup.find(itemprop='availability')
            if (Data):
                if (Data.get('href')):
                    Val = Data.get('href')
                elif (Data.get('content')):
                    Val = Data.get('content')
                return 'InStock' in Val

    def Price(self) -> list:
        Soup = self.Soup.find(itemprop='offers')
        if (Soup):
            Data = Soup.find(itemprop='price')
            if (Data):
                Val = Data.get('content')
                if (not Val):
                    Val = Data.text.strip()

                return [
                    float(Val),
                    Soup.find(itemprop='priceCurrency').get('content')
                ]

    def Features(self) -> dict:
        Soup = self.Soup.find_all(itemtype=re.compile('://schema.org/PropertyValue'))
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

    def Category(self) -> str:
        Soup = self.Soup.find(itemprop='category')
        if (Soup):
            return Soup.get('content')
        else:
            Soup = self.Soup.find(itemtype=re.compile('://schema.org/BreadcrumbList'))
            if (Soup):
                ListLI = Soup.find_all(itemtype=re.compile('://schema.org/ListItem'))
                if (ListLI):
                    Res = []
                    for xListLI in ListLI:
                        Val = xListLI.find(itemprop='name')
                        if (Val):
                            Res.append(Val.text.strip())
                    return '/'.join(Res)
