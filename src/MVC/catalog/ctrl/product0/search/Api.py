# Created: 2023.03.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import GetDictDefs, TDbList, TPagination
from ..._inc.products_a import Main as products_a


async def ajax(self, aData: dict = None) -> dict:
    aSearch, aLang = GetDictDefs(
        aData,
        ('q', 'lang'),
        ('', 'ua')
    )

    Dbl = await self.ExecModelImport(
        'ref_product0/product',
        {
            'method': 'Get_Products_LangAjax',
            'param': {
                'aLangId': self.GetLangId(aLang),
                'aFilter': aSearch
            }
        }
    )
    if (Dbl):
        Res = Dbl.ExportList('title')
        return Res

async def Main(self, aData: dict = None) -> dict:
    aSearch, aLang, aSort, aOrder, aPage, aLimit = GetDictDefs(
        aData.get('query'),
        ('q', 'lang', 'sort', 'order', 'page', 'limit'),
        ('', 'ua', ('sort_order, title', 'title', 'price'), ('asc', 'desc'), 1, 18)
    )

    await self.Lang.Add(aLang, 'product/category')

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
        Data = TPagination(aLimit, f'?route=product0/search&q={aSearch}&page={{page}}').Get(Dbl.Rec.total, aPage)
        DblPagination = TDbList(['page', 'title', 'href', 'current'], Data)

        DblProducts = await products_a(self, Dbl)

        Res = {
            'dbl_products_a': DblProducts.Export(),
            'dbl_pagenation': DblPagination.Export()
        }
        return Res
