# Created: 2023.10.26
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import GetDictDefs, TPagination, TDbList
from ..._inc.products_a import Main as products_a
from ..._inc import GetBreadcrumbs


async def Main(self, aData: dict = None) -> dict:
    aCategoryId, aLang, aSort, aOrder, aPage, aLimit = GetDictDefs(
        aData.get('query'),
        ('category_id', 'lang', 'sort', 'order', 'page', 'limit'),
        ('0', 'ua', ('sort_order, title', 'title', 'price'), ('asc', 'desc'), 1, 18)
    )
    aLimit = min(aLimit, 50)
    aLangId = self.GetLangId(aLang)

    Dbl = await self.ExecModelImport(
        'ref_product0/category',
        {
            'method': 'Get_CategoryIds_Sub',
            'param': {'aCategoryIds': [aCategoryId]}
        }
    )
    if (not Dbl):
        return {'err_code': 404}

    CategoryIds = Dbl.ExportList('id')
    Dbl = await self.ExecModelImport(
        'ref_product0/category',
        {
            'method': 'Get_CategoriesProducts_LangImagePrice',
            'param': {
                'aCategoryIds': CategoryIds,
                'aLangId': aLangId,
                'aPriceId': 1,
                'aOrder': f'{aSort} {aOrder}',
                'aLimit': aLimit,
                'aOffset': (aPage - 1) * aLimit
            }
        }
    )
    if (not Dbl):
        return {'err_code': 404}

    Data = TPagination(aLimit, f'?route=product0/category&category_id={aCategoryId}').Get(Dbl.Rec.total, aPage)
    DblPagination = TDbList(['page', 'title', 'href', 'current'], Data)

    DblProducts = await products_a(self, Dbl)

    DblCategory = await self.ExecModelImport(
        'ref_product0/category',
        {
            'method': 'Get_Category_LangId',
            'param': {
                'aCategoryId': aCategoryId,
                'aLangId': aLangId
            }
        }
    )
    Category = DblCategory.Rec.GetAsDict()
    BreadCrumbs = await GetBreadcrumbs(self, aLangId, aCategoryId)

    Res = {
        'dbl_products_a': DblProducts.Export(),
        'dbl_pagenation': DblPagination.Export(),
        'category': Category,
        'breadcrumbs': BreadCrumbs,
        'info': {
            'title': Category['title'],
            'count': Dbl.Rec.total,
            'page': aPage
        }
    }
    return Res
