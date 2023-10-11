# Created: 2023.04.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import json
from IncP.LibCtrl import TDbSql, GetDictDefs
from .Features import TFeatures


async def Main(self, aData: dict = None) -> dict:
    async def GetBreadcrumbs(aLang: str, aCategoryIdt: int, aTenantId: int) -> dict:
        Data = await self.ExecModel(
            'ref_product/category',
            {
                'method': 'Get_CategoryIdt_Path',
                'param': {'aLang': aLang, 'aCategoryIdts': [aCategoryIdt], 'aTenantId': aTenantId}
            }
        )

        Res = []
        DblData = Data.get('data')
        if (DblData):
            Res = []
            Path = '0'
            Dbl = TDbSql().Import(DblData)
            for Title, Idt in zip(Dbl.Rec.path_title, Dbl.Rec.path_idt):
                Path += f'_{Idt}'
                Res.append({'href': f'?route=product/category&path={Path}', 'title': Title})
        return Res

    async def GetImages(aImages: list[str]) -> dict:
        Res = []
        if (aImages):
            Images = [f'product/{x}' for x in aImages]
            ResEI = await self.ExecImg(
                'system',
                {
                    'method': 'GetImages',
                    'param': {'aFiles': Images}
                }
            )

            Images = ResEI['image']
            if (Images):
                Res = {'image': Images[0], 'images': Images}

        if (not Res):
            Res = {'image': 'http://ToDo/NoImage.jpg', 'images': []}
        return Res

    aPath, aLang, aProductId, aTenantId = GetDictDefs(
        aData.get('query'),
        ('path', 'lang', 'product_id', 'tenant'),
        ('0', 'ua', 0, 1)
    )

    Res = await self.ExecModel(
        'ref_product/product',
        {
            'method': 'Get_Product0_LangId',
            'param': {'aLang': aLang, 'aProductId': aProductId}
        }
    )

    DblData = Res.get('data')
    if (DblData):
        del Res['data']

        Dbl = TDbSql().Import(DblData)
        Product = Dbl.Rec.GetAsDict()

        Features = Product.get('features', {})
        Product['features'] = TFeatures(aLang).Adjust(Features)

        Images = await GetImages(Dbl.Rec.images)
        Product.update(Images)

        Product['price'] = await self.ExecModelExport(
            'ref_product/price',
            {
                'method': 'Get_Price_Product',
                'param': {'aProductId': aProductId, 'aPriceType': ['sale']}
            }
        )

        Product['price_hist'] = await self.ExecModelExport(
            'ref_product/price',
            {
                'method': 'Get_PriceHist_Product',
                'param': {'aProductId': aProductId}
            }
        )

        CategoryIdt = list(map(int, aPath.split('_')))[-1]
        Product['breadcrumbs'] = await GetBreadcrumbs(aLang, CategoryIdt, aTenantId)

        SchemaProduct = {
            '@context': 'https://schema.org/',
            '@type': 'Product',
            'image': Product.get('images'),
            'name': Product.get('title'),
            'description': Product.get('descr'),
            'offers': {
                '@type': 'Offer',
                'itemCondition': 'https://schema.org/NewCondition',
                'availability': 'https://schema.org/InStock',
                'price': 123.45,
                'priceCurrency': 'uah'
            }
        }
        Product['schema'] = json.dumps(SchemaProduct)

        Res['href'] = {
            'tenant': f'?tenant={aTenantId}'
        }

        Res['product'] = Product
    return Res
