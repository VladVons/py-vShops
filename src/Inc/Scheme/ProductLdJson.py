# Created: 2024.09.27
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from bs4 import BeautifulSoup
#
from Inc.Var.Dict import DeepGetByList, FilterNotNone
from Inc.Var.Str import ToJson


class TProductLdJson():
    def __init__(self, aSoup: BeautifulSoup):
        self.Root = aSoup
        self.Soup = aSoup.find_all('script', type='application/ld+json')

    def _AtType(self, aData: dict) -> list:
        Res = {}
        match aData['@type']:
            case 'Product':
                R = self._JProduct(aData)
                if (R):
                    Res.update(R)
            case 'BreadcrumbList':
                R = self._JBreadcrumbList(aData)
                if (R):
                    Res.update({'category': R})
            case 'ImageGallery':
                R = self._JImageGallery(aData)
                if (R):
                    Res.update({'images': R})
        return FilterNotNone(Res)

    def Parse(self, aMaxCnt: int = 99) -> list:
        Res = []
        if (self.Soup):
            for Idx, xSoup in enumerate(self.Soup):
                if (Idx > aMaxCnt):
                    break

                Data = xSoup.text.strip()
                Data = ToJson(Data)
                if (isinstance(Data, dict)):
                    if ('@type' in Data):
                        R = self._AtType(Data)
                        if (R):
                            Res.append(R)
                    elif ('@graph' in Data):
                        Graph = Data.get('@graph')
                        for xGraph in Graph:
                            R = self._AtType(xGraph)
                            if (R):
                                Res.append(R)
        return Res

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
                Res['price'] = [
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
            Val = aData.get('brand')
            if (not Val) or (isinstance(Val, dict)):
                Val = DeepGetByList(aData, ['brand', 'name'])
            Res['brand'] = Val

        if ('mpn' in aData):
            Val = aData['mpn']
            if (Val):
                Res['mpn'] = Val

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
