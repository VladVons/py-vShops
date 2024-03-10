# Created: 2023.10.26
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import GetDictDefs, TPagination, TDbList, IsDigits, DeepGetByList
from ..._inc.products_a import Main as products_a
from ..._inc import GetBreadcrumbs, GetProductsSort


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

    Attr = {}
    AttrArr = []
    if (aAttr):
        for Group in aAttr.strip('[]').split(';;'):
            if (Group):
                Pair = Group.split(':')
                if (len(Pair) == 2):
                    AttrId, Val = Pair
                    Attr[AttrId] = Val.split(';')
                    AttrArr.append(Val)

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

    Title = f"{DeepGetByList(aData, ['lang', 'category'], '')}: {Category['title']} {';'.join(AttrArr)} ({DblProducts.Rec.total}) - {DeepGetByList(aData, ['lang', 'page'], '') } {aPage}"

    HrefCanonical = f'?route=product0/category&category_id={aCategoryId}'
    Pagination = TPagination(aLimit, aData['path_qs'])
    PData = Pagination.Get(Dbl.Rec.total, aPage)
    DblPagination = TDbList(['page', 'title', 'href', 'current'], PData)

    dbl_products_a_sort = GetProductsSort(Pagination.Href, f'&sort={aSort}&order={aOrder}', aData['lang'])

    Res = {
        'dbl_products_a': DblProducts.Export(),
        'dbl_products_a_title': Title,
        'dbl_products_a_sort': dbl_products_a_sort.Export(),
        'dbl_pagenation': DblPagination.Export(),
        'category': Category,
        'breadcrumbs': BreadCrumbs,
        'canonical': HrefCanonical,
        'title': Title
    }
    return Res
