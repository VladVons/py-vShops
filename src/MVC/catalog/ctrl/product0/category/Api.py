# Created: 2023.10.26
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import math
#
from IncP.LibCtrl import GetDictDefs
from ..._inc.products_a import Main as products_a

async def Main(self, aData: dict = None) -> dict:
    aCategoryId, aLang, aSort, aOrder, aPage, aLimit = GetDictDefs(
        aData.get('query'),
        ('category_id', 'lang', 'sort', 'order', 'page', 'limit'),
        ('0', 'ua', ('sort_order, title', 'title', 'price'), ('asc', 'desc'), 1, 18)
    )
    aLimit = min(aLimit, 50)

    Dbl = await self.ExecModelImport(
        'ref_product0/category',
        {
            'method': 'Get_CategoryIds_Sub',
            'param': {'aCategoryIds': [aCategoryId]}
        }
    )
    if (not Dbl):
        return {'total': 0}

    CategoryIds = Dbl.ExportList('id')

    Dbl = await self.ExecModelImport(
        'ref_product0/category',
        {
            'method': 'Get_CategoriesProducts_LangImagePrice',
            'param': {'aCategoryIds': CategoryIds, 'aLang': aLang, 'aPriceId': 1, 'aOrder': f'{aSort} {aOrder}', 'aLimit': aLimit, 'aOffset': (aPage - 1) * aLimit}
        }
    )
    if (not Dbl):
        return

    Dbl = await products_a(self, Dbl)
    return {'dbl_products_a': Dbl.Export()}
