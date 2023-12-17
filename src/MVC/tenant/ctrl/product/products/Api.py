# Created: 2023.12.17
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.DbList import TDbList
from Inc.Misc.Pagination import TPagination
from Inc.Util.Obj import DeepGetByList
from IncP.LibCtrl import GetDictDefs
from ..._inc.products_b import Main as products_b


async def Main(self, aData: dict = None) -> dict:
    aSearch, aLang, aSort, aOrder, aPage, aLimit = GetDictDefs(
        aData.get('query'),
        ('q', 'lang', 'sort', 'order', 'page', 'limit'),
        ('', 'ua', ('sort_order, title', 'title', 'price'), ('asc', 'desc'), 1, 25)
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
                'aFilter': aSearch,
                'aOrder': f'{aSort} {aOrder}',
                'aLimit': aLimit,
                'aOffset': (aPage - 1) * aLimit
            }
        }
    )

    if (Dbl):
        Data = TPagination(aLimit, f'/{self.Name}/?route=product/products&q={aSearch}&page={{page}}').Get(Dbl.Rec.total, aPage)
        DblPagination = TDbList(['page', 'title', 'href', 'current'], Data)

        DblProducts = await products_b(self, Dbl)

        Res = {
            'dbl_products_b': DblProducts.Export(),
            'dbl_pagenation': DblPagination.Export()
        }
        return Res
