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

    if (not Product['descr']) and (Product['category_id']):
        DblDescrRnd = await self.ExecModelImport(
            'ref_product0/category',
            {
                'method': 'Get_CategoryDescrRnd',
                'param': {
                    'aCategoryId': Product['category_id'],
                    'aLangId': aLangId
                }
            }
        )

        if (DblDescrRnd):
            # Env = Environment()
            # Template = Env.from_string(DblDescrRnd.Rec.descr)
            # Product['descr'] = Template.render({
            #     'product_title': Product['title']
            # })
            Product['descr'] = DblDescrRnd.Rec.descr
        else:
            Product['descr'] = f"{Product['category_title']} {Product['title']} {', '.join(Descr)}"
    Product['descr'] = Lib.HtmlEsc(Product['descr'])

    if (Product['review']):
        Product['review'] = Lib.TDbList(['public_date', 'rating', 'descr'], Product['review']).Export()

    if (Product['meta_descr']):
        Res['meta_descr'] = Product['meta_descr']
    else:
        Res['meta_descr'] = Lib.ResGetItem(aData, 'meta_descr')

    DblAttr.AddFieldsFill(['href'], False)
    for Idx, Rec in enumerate(DblAttr):
        DblAttr.RecMerge([Hrefs[Idx]])
    Product['attr'] = DblAttr.Export()

    Features = Product.get('features') or {}
    #Product['features'] = TFeatures(aLang).Adjust1(Features)
    Product['features'] = Features

    Images = await self.GetImages(Product['images'])
    Product.update(Images)

    DblPriceSale = await self.ExecModelImport(
        'ref_product/price',
        {
            'method': 'Get_Price_Product',
            'param': {
                'aProductId': aProductId,
                'aPriceType': ['sale']
            }
        }
    )
    Product['price'] = DblPriceSale.Export()
    Product['price_sale'] = f'{DblPriceSale.Rec.price} {DblPriceSale.Rec.alias}'

    DblPriceHist = await self.ExecModelImport(
        'ref_product/price',
        {
            'method': 'Get_PriceHist_Product',
            'param': {'aProductId': aProductId}
        }
    )
    Product['price_hist'] = DblPriceHist.Export()

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
            'price': DblPriceSale.Rec.price,
            'priceCurrency': DblPriceSale.Rec.alias
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

    if (not Product['meta_title']):
        Res['meta_title'] = f"{Product['category_title']} {Product['title']}"

    Res['product'] = Product

    DictRepl = Lib.TDictReplDeep(Res)
    Res['meta_descr'] = DictRepl.Parse(Res['meta_descr'])
    Product['descr'] = DictRepl.Parse(Product['descr'])
    Product['rest'] = Lib.HideDigit(Product['rest'])

    return Res
