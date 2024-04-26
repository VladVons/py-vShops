# Created: 2023.10.26
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib
from ..._inc.products_a import Main as products_a
from ..._inc import GetBreadcrumbs, GetProductsSort


def FindAttrFilter(aDbl: Lib.TDbList, aAttr: dict, aCategoryId: int) -> list[str]:
    Res = []
    for Rec in aDbl:
        if (Rec.category_id == int(aCategoryId)):
            Filter = {}
            for AttrId, Val, _ in Rec.filter:
                if (AttrId not in Filter):
                    Filter[AttrId] = []
                Filter[AttrId].append(Val)

            Found = True
            for Key, Val in aAttr.items():
                FilterVal = Filter.get(Key, [])
                if (not any(x in Val for x in FilterVal)):
                    Found = False
                    break
            if (Found):
                Res.append(Rec.title)
    return Res


async def Main(self, aData: dict = None) -> dict:
    aCategoryId, aLang, aAttr, aSort, aOrder, aPage, aLimit = Lib.GetDictDefs(
        aData.get('query'),
        ('category_id', 'lang', 'attr', 'sort', 'order', 'page', 'limit'),
        ('0', 'ua', '', ('sort_order, title', 'title', 'price'), ('asc', 'desc'), 1, 18)
    )

    if (not Lib.IsDigits([aCategoryId, aPage, aLimit])):
        return {'status_code': 404}

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
        return {'status_code': 404}

    AttrDescr = ''
    Attr = Lib.AttrDecode(aAttr)
    if (Attr):
        DblAttr = await self.ExecModelImport(
            'ref_attr',
            {
                'method': 'Get_AttrFilter',
                'param': {}
            }
        )
        AttrFilter = FindAttrFilter(DblAttr, Attr, aCategoryId)
        if (AttrFilter):
            AttrDescr = Lib.ResGetLang(aData, 'appointment') + ': ' + ', '.join(AttrFilter)

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
        return {'status_code': 404}

    Res = {}
    DblProducts = await products_a(self, Dbl)
    Res['dbl_products_a'] = DblProducts.Export()

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
    Res.update(DblCategory.Rec.GetAsDict())
    if (not Res['meta_descr']):
        Res['meta_descr'] = f"{Res['title']}, {Lib.ResGetLang(aData, 'meta_descr')}"

    Res['breadcrumbs'] = await GetBreadcrumbs(self, aLangId, aCategoryId)
    ModCategoryAttr = Lib.ResGetModule(aData, 'category_attr')
    Title = f"{Lib.ResGetLang(aData, 'category')}: {Res['title']} ({DblProducts.Rec.total}) - {Lib.ResGetLang(aData, 'page')} {aPage}"
    Res['title'] = Res['products_a_title'] = Title
    Res['products_a_descr'] = [ModCategoryAttr.get('descr', ''), AttrDescr]

    if (self.ApiCtrl.Conf.get('seo_url')):
        Href = await Lib.SeoEncodeStr(self, Lib.UrlEncode(aData['query']))
    else:
        Href = aData['path_qs']

    Pagination = Lib.TPagination(aLimit, Href)
    PData = Pagination.Get(Dbl.Rec.total, aPage)
    DblPagination = Lib.TDbList(['page', 'title', 'href', 'current'], PData)
    Res['dbl_pagenation'] = DblPagination.Export()

    dbl_products_a_sort = GetProductsSort(Pagination.Href, f'&sort={aSort}&order={aOrder}', aData['res']['lang'])
    Res['dbl_products_a_sort'] = dbl_products_a_sort.Export()

    return Res
