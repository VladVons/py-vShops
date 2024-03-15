# Created: 2023.10.26
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import GetDictDefs, TPagination, TDbList, IsDigits, FindModule, FindLang
from ..._inc.products_a import Main as products_a
from ..._inc import GetBreadcrumbs, GetProductsSort


def AttrDecode(aVal: str) -> dict:
    Res = {}
    if (aVal):
        for Group in aVal.strip('[]').split(';;'):
            if (Group):
                Pair = Group.split(':')
                if (len(Pair) == 2):
                    AttrId, Val = Pair
                    Res[AttrId] = Val.split(';')
    return Res

async def Main(self, aData: dict = None) -> dict:
    aCategoryId, aLang, aAttr, aSort, aOrder, aPage, aLimit = GetDictDefs(
        aData.get('query'),
        ('category_id', 'lang', 'attr', 'sort', 'order', 'page', 'limit'),
        ('0', 'ua', '', ('sort_order, title', 'title', 'price'), ('asc', 'desc'), 1, 18)
    )

    if (not IsDigits([aCategoryId, aPage, aLimit])):
        return {'err_code': 404}

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

    Attr = AttrDecode(aAttr)
    if (not IsDigits(Attr.keys())):
        return {'err_code': 404}

    CategoryIds = Dbl.ExportList('id')
    Dbl = await self.ExecModelImport(
        'ref_product0/category',
        {
            'method': 'Get_CategoriesProducts_LangImagePrice',
            'param': {
                'aCategoryIds': CategoryIds,
                'aLangId': aLangId,
                'aAttr': Attr,
                'aPriceId': 1,
                'aOrder': f'{aSort} {aOrder}',
                'aLimit': aLimit,
                'aOffset': (aPage - 1) * aLimit
            }
        }
    )
    if (not Dbl):
        return {'err_code': 404}

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

    ModCategoryAttr = FindModule(aData, 'category_attr')
    if (ModCategoryAttr):
        DblAttr = TDbList().Import(ModCategoryAttr['dbl_category_attr'])
    else:
        DblAttr = await self.ExecModelImport(
            'ref_product0/category',
            {
                'method': 'Get_CategoryAttr',
                'param': {
                    'aLangId': aLangId,
                    'aCategoryId': aCategoryId
                }
            }
        )
    AttrPair = DblAttr.ExportPair('attr_id', 'title')
    AttrArr = [AttrPair.get(int(Key), '') + ': ' + ';'.join(Val) for Key, Val in Attr.items()]

    Title = f"{FindLang(aData, 'category')}: {Category['title']} ({DblProducts.Rec.total}) - {FindLang(aData, 'page')} {aPage}"

    HrefCanonical = f'?route=product0/category&category_id={aCategoryId}'
    Pagination = TPagination(aLimit, aData['path_qs'])
    PData = Pagination.Get(Dbl.Rec.total, aPage)
    DblPagination = TDbList(['page', 'title', 'href', 'current'], PData)

    dbl_products_a_sort = GetProductsSort(Pagination.Href, f'&sort={aSort}&order={aOrder}', aData['res']['lang'])

    Res = {
        'dbl_products_a': DblProducts.Export(),
        'products_a_title': Title,
        'products_a_descr': ', '.join(AttrArr),
        'dbl_products_a_sort': dbl_products_a_sort.Export(),
        'dbl_pagenation': DblPagination.Export(),
        'category': Category,
        'breadcrumbs': BreadCrumbs,
        'canonical': HrefCanonical,
        'title': Title
    }
    return Res
