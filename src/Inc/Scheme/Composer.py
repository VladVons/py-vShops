# Created: 2024.09.27
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re

import json
from bs4 import BeautifulSoup
#
from Inc.Var.Dict import DeepGetByList


class TComposer():
    def __init__(self, aSite: str, aData: str):
        self.Site = aSite
        self.Macros = {}
        self.Soup = BeautifulSoup(aData, 'html.parser')

    def _Update(self, aCheck, aData):
        if (aCheck):
            self.Macros.update(aData)

    def _TableFeatures(self):
        Data = self.Soup.find('table', class_=re.compile(r'(features|attributes)'))
        if (Data):
            Attr = Data.attrs
            Tr = []
            for Row in Data.find_all('tr'):
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
            self.Macros['features'] = Res

    def _JBreadcrumbList(self, aData):
        Res = []
        for xItem in aData.get('itemListElement'):
            if (xItem.get('@type') == 'ListItem'):
                Val = DeepGetByList(xItem, ['item', 'name'])
                if (not Val):
                    Val = xItem.get('name')
                Res.append(Val)
        self._Update(Res, {'category': '/'.join(Res)})

    def _JProduct(self, aData):
        def AtOffers(aOffers: dict):
            if ('price' in aOffers):
                Res['price'] = [
                    float(aOffers['price']),
                    aOffers.get('priceCurrency')
                ]

            if ('lowPrice' in aOffers):
                Res['Price'] = [
                    float(aOffers['lowPrice']),
                    aOffers.get('priceCurrency')
                ]

            if ('availability' in aOffers):
                Res['stock'] = ('InStock' in aOffers['availability'])

        Res = {}
        if ('category' in aData):
            Res['category'] = aData['category']

        if ('name' in aData):
            Res['name'] = aData['name']

        if ('brand' in aData):
            Res['brand'] = DeepGetByList(aData, ['brand', 'name'])

        if ('image' in aData):
            Data = aData['image']
            if (isinstance(Data, list)):
                Res['images'] = Data
            else:
                Res['image'] = Data

        if ('offers' in aData):
            Offers = aData['offers']
            if (isinstance(Offers, dict)):
                AtOffers(Offers)
            elif (isinstance(Offers, list)):
                for xOffer in Offers:
                    AtOffers(xOffer)

        self._Update(Res, Res)

    def _JImageGallery(self, aData):
        Res = []
        for xItem in aData.get('associatedMedia', []):
            if (xItem.get('@type') == 'ImageObject'):
                Val = xItem.get('contentUrl')
                Res.append(Val)
        self._Update(Res, {'images': Res})

    def _AppLdJson(self):
        def AtType(aData):
            Type = aData['@type']
            if (Type == 'Product'):
                self._JProduct(aData)
            elif (Type == 'BreadcrumbList'):
                self._JBreadcrumbList(aData)
            elif (Type == 'ImageGallery'):
                self._JImageGallery(aData)

        Soup = self.Soup.find_all('script', type='application/ld+json')
        if (not Soup):
            return

        for xSoup in Soup:
            Data = json.loads(xSoup.string)
            if (isinstance(Data, dict)):
                if ('@type' in Data):
                    AtType(Data)
                elif ('@graph' in Data):
                    Graph = Data.get('@graph')
                    for xGraph in Graph:
                        AtType(xGraph)

    def _ITBreadcrumbList(self):
        Res = []
        ListBS = self.Soup.find(itemtype=re.compile('://schema.org/BreadcrumbList'))
        if (ListBS):
            ListLI = ListBS.find_all(itemtype=re.compile('://schema.org/ListItem'))
            if (ListLI):
                for xListLI in ListLI:
                    Val = xListLI.find(itemprop='name')
                    if (Val):
                        Res.append(Val.text.strip())
        self._Update(Res, {'category': '/'.join(Res)})

    def _ITProduct(self):
        Product = self.Soup.find(itemtype=re.compile('://schema.org/Product'))
        if (Product):
            Data = Product.find(itemprop='name')
            if (Data):
                Val = Data.get('content')
                if (not Val):
                    Val = Data.text.strip()
                    if (len(Val) < 10):
                        Data = Product.find('h1', itemprop='name')
                        if (Data):
                            Val = Data.text.strip()
                self.Macros['name'] = Val

            Data = Product.find(itemprop='category')
            if (Data):
                self.Macros['category'] = Data.get('content')

            Data = Product.find_all(itemprop='image')
            if (Data):
                Res = []
                for xData in Data:
                    if (xData.get('href')):
                        Val = xData.get('href')
                    elif (xData.get('src')):
                        Val = xData.get('src')

                    if (not Val.startswith('http')):
                        Val = self.Site + Val
                    Res.append(Val)

                self.Macros['images'] = Res

            Offers = Product.find(itemprop='offers')
            if (Offers):
                Data = Offers.find(itemprop='availability')
                if (Data):
                    if (Data.get('href')):
                        Val = Data.get('href')
                    elif (Data.get('content')):
                        Val = Data.get('content')
                    self.Macros['stock'] = 'InStock' in Val

                Data = Offers.find(itemprop='price')
                if (Data):
                    Val = Data.get('content')
                    if (not Val):
                        Val = Data.text.strip()

                    self.Macros['price'] = [
                        float(Val),
                        Offers.find(itemprop='priceCurrency').get('content')
                    ]

            Property = Product.find_all(itemtype=re.compile('://schema.org/PropertyValue'))
            if (Property):
                Res = []
                for xProperty in Property:
                    Val = [
                        xProperty.find(itemprop='name').text.strip(),
                        xProperty.find(itemprop='value').text.strip()
                    ]
                    Res.append(Val)
                self.Macros['features'] = {Key:Val for Key, Val in Res}

    def _ItemType(self):
        self._ITProduct()
        self._ITBreadcrumbList()

    def _TryFind(self):
        self._TableFeatures()

    def Parse(self):
        self._AppLdJson()
        self._ItemType()
        self._TryFind()
