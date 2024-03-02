# Created: 2024.02.23
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import GetDictDefs, TPagination, TDbList, IsDigits
from ..._inc.products_a import Main as products_a


async def Main(self, aData: dict = None) -> dict:
    aTenantId, aLang, aSort, aOrder, aPage, aLimit = GetDictDefs(
        aData.get('query'),
        ('tenant_id', 'lang', 'sort', 'order', 'page', 'limit'),
        ('1', 'ua', ('sort_order, title', 'title', 'price'), ('asc', 'desc'), 1, 18)
    )

    if (not IsDigits([aTenantId, aPage, aLimit])):
        return {'err_code': 404}

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
        return {'err_code': 404}

    Data = TPagination(aLimit, f'?route=product0/tenant&tenant_id={aTenantId}').Get(Dbl.Rec.total, aPage)
    DblPagination = TDbList(['page', 'title', 'href', 'current'], Data)

    DblProducts = await products_a(self, Dbl)

    Res = {
        'dbl_products_a': DblProducts.Export(),
        'dbl_pagenation': DblPagination.Export(),
        'tenant': {},
        'info': {
            'title': Dbl.Rec.tenant_title,
            'count': Dbl.Rec.total,
            'page': aPage
        }
    }
    return Res
