# Created: 2024.09.27
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
from bs4 import BeautifulSoup
#
from Inc.Var.Dict import DeepGetByList, FilterNotNone


class TProductLdJson():
    def __init__(self, aSoup: BeautifulSoup):
        self.Soup = aSoup.find_all('script', type='application/ld+json')

    def Parse(self):
        def AtType(aData) -> dict:
            nonlocal Res
            Type = aData['@type']
            if (Type == 'Product'):
                R = self._JProduct(aData)
                if (R):
                    Res.update(R)
            elif (Type == 'BreadcrumbList'):
                R = self._JBreadcrumbList(aData)
                if (R):
                    Res.update({'category': R})
            elif (Type == 'ImageGallery'):
                R = self._JImageGallery(aData)
                if (R):
                    Res.update({'images': R})

        Res = {}
        if (self.Soup):
            for xSoup in self.Soup:
                Data = json.loads(xSoup.string)
                if (isinstance(Data, dict)):
                    if ('@type' in Data):
                        AtType(Data)
                    elif ('@graph' in Data):
                        Graph = Data.get('@graph')
                        for xGraph in Graph:
                            AtType(xGraph)
        return FilterNotNone(Res)

    def _JBreadcrumbList(self, aData) -> str:
        Items = aData.get('itemListElement')
        if (Items):
            Res = []
            for xItem in Items:
                if (xItem.get('@type') == 'ListItem'):
                    Val = DeepGetByList(xItem, ['item', 'name'])
                    if (not Val):
                        Val = xItem.get('name')
                    Res.append(Val)
            return '/'.join(Res)

    def _JProduct(self, aData) -> dict:
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

        if ('mpn' in aData):
            Res['mpn'] = aData['mpn']

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
        return Res

    def _JImageGallery(self, aData) -> list:
        Res = []
        for xItem in aData.get('associatedMedia', []):
            if (xItem.get('@type') == 'ImageObject'):
                Val = xItem.get('contentUrl')
                Res.append(Val)
        return Res
