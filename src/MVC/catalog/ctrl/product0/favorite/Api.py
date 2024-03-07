# Created: 2024.03.06
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import GetDictDefs, IsDigits
from ..._inc.products_a import Main as products_a


async def Main(self, aData: dict = None) -> dict:
    aProductIds, aLang, = GetDictDefs(
        aData.get('query'),
        ('product_ids', 'lang'),
        ('', 'ua')
    )

    ProductIds = aProductIds.strip('[]').split(';')
    if (not IsDigits(ProductIds)):
        return {'err_code': 404}

    aLangId = self.GetLangId(aLang)
    Dbl = await self.ExecModelImport(
        'ref_product0/product',
        {
            'method': 'Get_ProductsAttr',
            'param': {
                'aLangId': aLangId,
                'aProductIds': ProductIds
            }
        }
    )
    if (not Dbl):
        return {'err_code': 404}

    DblProducts = await products_a(self, Dbl)
    return {
        'dbl_products_a': DblProducts.Export()
    }
