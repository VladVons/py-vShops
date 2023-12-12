# Created: 2023.12.11
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.DbList import TDbList
from Inc.Misc.Pagination import TPagination
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
        return

    CategoryIds = Dbl.ExportList('id')

    Dbl = await self.ExecModelImport(
        'ref_product0/category',
        {
            'method': 'Get_CategoriesProducts_LangImagePrice',
            'param': {'aCategoryIds': CategoryIds, 'aLangId': self.GetLangId(aLang), 'aPriceId': 1, 'aOrder': f'{aSort} {aOrder}', 'aLimit': aLimit, 'aOffset': (aPage - 1) * aLimit}
        }
    )
    if (Dbl):
        Data = TPagination(aLimit, f'?route=product0/category&category_id={aCategoryId}&page={{page}}').Get(Dbl.Rec.total, aPage)
        DblPagination = TDbList(['page', 'title', 'href', 'current'], Data)

        DblProducts = await products_a(self, Dbl)

        Res = {
            'dbl_products_a': DblProducts.Export(),
            'dbl_pagenation': DblPagination.Export()
        }
        return Res
