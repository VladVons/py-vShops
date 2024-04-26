# Created: 2023.04.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
#
import IncP.LibCtrl as Lib
#from .Features import TFeatures
from ..._inc import GetBreadcrumbs


async def Main(self, aData: dict = None) -> dict:
    aLang, aProductId = Lib.GetDictDefs(
        aData.get('query'),
        ('lang', 'product_id'),
        ('ua', 0)
    )

    if (not Lib.IsDigits([aProductId])):
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

    DblAttr = Lib.TDbList(['id', 'alias', 'title', 'val'], Product['attr'])
    Hrefs = []
    Descr = []
    for Rec in DblAttr:
        Hrefs.append(f'/?route=product0/category&category_id={CategoryId}&attr=[{Rec.id}:{Rec.val}]')
        Descr.append(f'{Rec.title}: {Rec.val}')

    if (self.ApiCtrl.Conf.get('seo_url')):
        Hrefs = await Lib.SeoEncodeList(self, Hrefs)

    if (not Product['descr']):
        Product['descr'] = f"{Product['category_title']} {Product['title']} {', '.join(Descr)}"
    Product['descr'] = Lib.HtmlEsc(Product['descr'])

    if (Product['meta_descr']):
        Res['meta_descr'] = Product['meta_descr']
    else:
        Res['meta_descr'] = f"{Product['title']}, {Lib.ResGetLang(aData, 'meta_descr')}"

    DblAttr.AddFieldsFill(['href'], False)
    for Idx, Rec in enumerate(DblAttr):
        DblAttr.RecMerge([Hrefs[Idx]])
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
        'category': Product['category_title'],
        'offers': {
            '@type': 'Offer',
            'itemCondition': 'https://schema.org/' + Lib.Iif(Product['cond_en'] == 'new', 'NewCondition', 'UsedCondition'),
            'availability': 'https://schema.org/' + Lib.Iif(Product['rest'] > 0, 'InStock', 'OutOfStock'),
            'price': DblPrice.Rec.price,
            'priceCurrency': DblPrice.Rec.alias
        }
    }
    Res['schema'] = json.dumps(Schema, ensure_ascii=False)

    Href = {
        'category': f'/?route=product0/category&category_id={CategoryId}',
        'tenant': f'/?route=product0/tenant&tenant_id={Product["tenant_id"]}',
        'canonical': f'/?route=product0/product&product_id={aProductId}'
    }
    if (self.ApiCtrl.Conf.get('seo_url')):
        Href = await Lib.SeoEncodeDict(self, Href)
    Href['self'] = aData['path_qs']
    Res['href'] = Href

    Res['product'] = Product
    Res['title'] = ''
    return Res
