# Created: 2023.04.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
#
from IncP.LibCtrl import GetDictDefs, Iif
from .Features import TFeatures
from ..._inc import GetBreadcrumbs


async def Main(self, aData: dict = None) -> dict:
    aLang, aProductId = GetDictDefs(
        aData.get('query'),
        ('lang', 'product_id'),
        ('ua', 0)
    )
    aLangId = self.GetLangId(aLang)

    DblProduct = await self.ExecModelImport(
        'ref_product0/product',
        {
            'method': 'Get_Product_LangId',
            'param': {
                'aLangId': aLangId,
                'aProductId': aProductId
            }
        }
    )
    if (not DblProduct):
        return {'err_code': 404}

    await self.ExecModel(
        'ref_product/product',
        {
            'method': 'Ins_HistProductView',
            'param': {
                'aProductId': aProductId,
                'aSessionId': aData['session']['session_id']
            }
        }
    )

    Res = {}
    Product = DblProduct.Rec.GetAsDict()

    Features = Product.get('features', {})
    Product['features'] = TFeatures(aLang).Adjust(Features)

    Images = await self.GetImages(Product['images'])
    Product.update(Images)

    Price = await self.ExecModelExport(
        'ref_product/price',
        {
            'method': 'Get_Price_Product',
            'param': {
                'aProductId': aProductId,
                'aPriceType': ['sale']
            }
        }
    )
    Product['price'] = Price

    DblPrice = await self.ExecModelImport(
        'ref_product/price',
        {
            'method': 'Get_PriceHist_Product',
            'param': {'aProductId': aProductId}
        }
    )
    Product['price_hist'] = DblPrice.Export()

    Res['breadcrumbs'] = await GetBreadcrumbs(self, aLangId, Product['category_id'])

    Schema = {
        '@context': 'https://schema.org/',
        '@type': 'Product',
        'image': Product['images'],
        'name': Product['title'],
        'description': Product['descr'],
        'offers': {
            '@type': 'Offer',
            'itemCondition': 'https://schema.org/' + Iif(Product['cond_en'] == 'new', 'NewCondition', 'UsedCondition'),
            'availability': 'https://schema.org/' + Iif(Product['rest'] > 0, 'InStock', 'OutOfStock'),
            'price': DblPrice.Rec.price,
            'priceCurrency': DblPrice.Rec.alias
        }
    }
    Res['schema'] = json.dumps(Schema)

    Res['href'] = {
        'self': aData['path_qs'],
        'category': f'?route=product0/category&category_id={Product["category_id"]}',
        'tenant': f'?route=product0/tenant&tenant_id={Product["tenant_id"]}'
    }

    Res['product'] = Product
    return Res
