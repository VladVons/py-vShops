# Created: 2023.12.17
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import TDbList, TPagination, DeepGetByList, GetDictDefs
from ..._inc.products_b import Main as products_b


async def Main(self, aData: dict = None) -> dict:
    aSearch, aFilter, aLang, aSort, aOrder, aPage, aLimit = GetDictDefs(
        aData.get('query'),
        ('search', 'filter', 'lang', 'sort', 'order', 'page', 'limit'),
        ('','', 'ua', ('sort_order, title', 'title', 'price'), ('asc', 'desc'), 1, 25)
    )

    #await self.Lang.Add(aLang, 'product/category')
    AuthId = DeepGetByList(aData, ['session', 'auth_id'])
    aLimit = min(aLimit, 50)

    Dbl = await self.ExecModelImport(
        'ref_product/product',
        {
            'method': 'Get_Products_LangFilter',
            'param': {
                'aLangId': self.GetLangId(aLang),
                'aTenantId': AuthId,
                'aSearch': aSearch,
                'aFilter': aFilter,
                'aOrder': f'{aSort} {aOrder}',
                'aLimit': aLimit,
                'aOffset': (aPage - 1) * aLimit
            }
        }
    )

    if (Dbl):
        Data = TPagination(aLimit, f'/{self.Name}?route=product/products&search={aSearch}&filter={aFilter}').Get(Dbl.Rec.total, aPage)
        DblPagination = TDbList(['page', 'title', 'href', 'current'], Data)

        DblProducts = await products_b(self, Dbl)

        Res = {
            'dbl_products_b': DblProducts.Export(),
            'dbl_pagenation': DblPagination.Export()
        }
        return Res
