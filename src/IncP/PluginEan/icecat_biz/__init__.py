# Created: 2023.06.08
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import aiohttp
#
from Inc.Util.Obj import DeepGetByList
from .. import TParserBase


class TParser(TParserBase):
    CodeType = 'icecat'
    UrlRoot = 'https://icecat.biz'
    SkipFeatures = {
        'пк/робочі станції': ["Пам'ять", 'Носії зберігання даних']
    }

    async def _GetData(self, aCode: str) -> dict:
        ShopName = 'VladVons'
        AppKey = '0Bu9AgccFpvGA44Lp2Uvp83rq41QlRF8'
        Url = f'https://live.icecat.biz/api?shopname={ShopName}&lang=uk&icecat_id={aCode}&app_key={AppKey}'
        #Url = 'https://icecat.biz/p/vendorName/mpn/desc-{aCode}.html'

        async with aiohttp.ClientSession() as Session:
            async with Session.get(Url) as Response:
                Data = await Response.json()
                if (Data.get('msg') == 'OK'):
                    Data = Data['data']
                    Name = f"{Data['GeneralInfo']['Brand']} {Data['GeneralInfo']['ProductName']}"
                    Images = [x.get('Pic') for x in Data['Gallery'] if x.get('Type') == 'ProductImage']
                    Category = DeepGetByList(Data, ['GeneralInfo', 'Category', 'Name', 'Value'], '').lower()

                    Features = {}
                    for xFG in Data['FeaturesGroups']:
                        Feature = xFG['FeatureGroup']['Name']['Value']
                        Skip = self.SkipFeatures.get(Category, {})
                        if (Feature not in Skip):
                            Features[Feature] = []
                            for xF in xFG['Features']:
                                Val = xF['PresentationValue']
                                Key = xF['Feature']['Name']['Value']
                                Features[Feature].append(f'{Key}: {Val}')

                    Res = {
                        'name': Name,
                        'images': Images,
                        'category': Category,
                        'features': Features
                    }
                    #self._WriteFile('ice-2.json', Data)
                    if (Res):
                        Res['url'] = Url
                    return Res
