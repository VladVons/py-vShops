# Created: 2023.03.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import GetDictDefs, TDbList, TPagination, IsDigits, ResGetLang, UrlEncode
from ..._inc.products_a import Main as products_a
from ..._inc import GetProductsSort


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

    if (not IsDigits([aPage, aLimit])):
        return {'status_code': 404}

    aLangId = self.GetLangId(aLang)
    aLimit = min(aLimit, 50)
    await self.Lang.Add(aLang, 'product/category')

    Dbl = await self.ExecModelImport(
        'ref_product0/product',
        {
            'method': 'Get_Products_LangFilter',
            'param': {
                'aLangId': aLangId,
                'aFilter': aSearch,
                'aOrder': f'{aSort} {aOrder}',
                'aLimit': aLimit,
                'aOffset': (aPage - 1) * aLimit
            }
        }
    )
    Found = Dbl.Rec.total if (Dbl) else 0

    await self.ExecModel(
        'ref_product/product',
        {
            'method': 'Ins_HistProductSearch',
            'param': {
                'aText': aSearch,
                'aResults': Found,
                'aLangId': aLangId,
                'aSessionId': aData['session']['session_id']
            }
        }
    )

    if (Found):
        Href = aData['path_qs']
        #Href = UrlEncode(aData['query'])

        Pagination = TPagination(aLimit, Href)
        PData = Pagination.Get(Dbl.Rec.total, aPage)
        DblPagination = TDbList(['page', 'title', 'href', 'current'], PData)

        DblProducts = await products_a(self, Dbl)
        Title = f"{ResGetLang(aData, 'search')}: {aSearch} ({Found}) - {ResGetLang(aData, 'page')} {aPage}"

        dbl_products_a_sort = GetProductsSort(Pagination.Href, f'&sort={aSort}&order={aOrder}', aData['res']['lang'])

        Res = {
            'dbl_products_a': DblProducts.Export(),
            'products_a_title': Title,
            'dbl_products_a_sort': dbl_products_a_sort.Export(),
            'dbl_pagenation': DblPagination.Export(),
            'title': Title,
        }
        return Res
