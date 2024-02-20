# Created: 2024.02.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import GetDictDefs, TDbList, TPagination
from ..._inc.products_b import Main as products_b


async def Main(self, aData: dict = None) -> dict:
    aSearch, aLang, aSort, aOrder, aPage, aLimit = GetDictDefs(
        aData.get('query'),
        ('search', 'lang', 'sort', 'order', 'page', 'limit'),
        ('', 'ua', 'product_title', 'asc', 1, 12)
    )

    if (not aSearch):
        return

    aLimit = min(aLimit, 50)

    Dbl = await self.ExecModelImport(
        'ref_product0/product',
        {
            'method': 'Get_Products_LangFilter',
            'param': {
                'aLangId': self.GetLangId(aLang),
                'aFilter': aSearch,
                'aOrder': f'{aSort} {aOrder}',
                'aLimit': aLimit,
                'aOffset': (aPage - 1) * aLimit
            }
        }
    )

    if (Dbl):
        Data = TPagination(aLimit, f'?route=product/search0&search={aSearch}').Get(Dbl.Rec.total, aPage)
        DblPagination = TDbList(['page', 'title', 'href', 'current'], Data)

        DblProducts = await products_b(self, Dbl)

        Res = {
            'dbl_products_b': DblProducts.Export(),
            'dbl_pagenation': DblPagination.Export()
        }
        return Res
