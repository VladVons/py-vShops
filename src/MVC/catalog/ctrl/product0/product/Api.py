# Created: 2023.04.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
#
from IncP.LibCtrl import GetDictDefs, Iif, IsDigits, TDbList
#from .Features import TFeatures
from ..._inc import GetBreadcrumbs


async def Main(self, aData: dict = None) -> dict:
    aLang, aProductId = GetDictDefs(
        aData.get('query'),
        ('lang', 'product_id'),
        ('ua', 0)
    )

    if (not IsDigits([aProductId])):
        return {'status_code': 404}

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
        return {'status_code': 404}

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
    CategoryId = Product['category_id']

    DblAttr = TDbList(['id', 'alias', 'title', 'val'], Product['attr'])
    DblAttr.AddFieldsFill(['href'], False)
    for Rec in DblAttr:
        Href = [
            f'/?route=product0/category&category_id={CategoryId}&attr=[{Rec.id}:{Rec.val}]'
        ]
        DblAttr.RecMerge(Href)
    Product['attr'] = DblAttr.Export()

    Features = Product.get('features') or {}
    #Product['features'] = TFeatures(aLang).Adjust1(Features)
    Product['features'] = Features

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

    Res['breadcrumbs'] = await GetBreadcrumbs(self, aLangId, CategoryId)

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
        'category': f'/?route=product0/category&category_id={CategoryId}',
        'tenant': f'/?route=product0/tenant&tenant_id={Product["tenant_id"]}'
    }

    Res['canonical'] = f'/?route=product0/product&product_id={aProductId}'

    Res['product'] = Product
    Res['title'] = ''
    return Res
