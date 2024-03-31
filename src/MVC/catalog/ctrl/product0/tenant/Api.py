# Created: 2024.02.23
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib
from ..._inc.products_a import Main as products_a
from ..._inc import GetProductsSort


async def Main(self, aData: dict = None) -> dict:
    aTenantId, aLang, aSort, aOrder, aPage, aLimit = Lib.GetDictDefs(
        aData.get('query'),
        ('tenant_id', 'lang', 'sort', 'order', 'page', 'limit'),
        ('1', 'ua', ('sort_order, title', 'title', 'price'), ('asc', 'desc'), 1, 18)
    )

    if (not Lib.IsDigits([aTenantId, aPage, aLimit])):
        return {'status_code': 404}

    aLangId = self.GetLangId(aLang)
    aLimit = min(aLimit, 50)

    Dbl = await self.ExecModelImport(
        'ref_product0/tenant',
        {
            'method': 'Get_TenantProducts_LangImagePrice',
            'param': {
                'aTenantId': aTenantId,
                'aLangId': aLangId,
                'aPriceId': 1,
                'aOrder': f'{aSort} {aOrder}',
                'aLimit': aLimit,
                'aOffset': (aPage - 1) * aLimit
            }
        }
    )
    if (not Dbl):
        return {'status_code': 404}

    Title = f"{Lib.ResGetLang(aData, 'tenant')}: {Dbl.Rec.tenant_title} ({Dbl.Rec.total}) - {Lib.ResGetLang(aData, 'page')} {aPage}"

    if (self.ApiCtrl.Conf.get('seo_url')):
        Href = await Lib.SeoEncodeStr(self, Lib.UrlEncode(aData['query']))
    else:
        Href = aData['path_qs']

    Pagination = Lib.TPagination(aLimit, Href)
    PData = Pagination.Get(Dbl.Rec.total, aPage)
    DblPagination = Lib.TDbList(['page', 'title', 'href', 'current'], PData)

    dbl_products_a_sort = GetProductsSort(Pagination.Href, f'&sort={aSort}&order={aOrder}', aData['res']['lang'])

    DblProducts = await products_a(self, Dbl)

    Res = {
        'dbl_products_a': DblProducts.Export(),
        'products_a_title': Title,
        'dbl_products_a_sort': dbl_products_a_sort.Export(),
        'dbl_pagenation': DblPagination.Export(),
        'title': Title
    }
    return Res
