# Created: 2023.03.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib
from ..._inc.products_a import Main as products_a
from ..._inc import GetProductsSort


async def ajax(self, aData: dict = None) -> dict:
    aSearch, aLang = Lib.GetDictDefs(
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
                'aFilter': aSearch.replace('_', ' ')
            }
        }
    )
    if (Dbl):
        Res = Dbl.ExportList('title')
        return Res

async def Main(self, aData: dict = None) -> dict:
    aSearch, aLang, aSort, aOrder, aPage, aLimit = Lib.GetDictDefs(
        aData.get('query'),
        ('q', 'lang', 'sort', 'order', 'page', 'limit'),
        ('', 'ua', ('sort_order, title', 'title', 'price'), ('asc', 'desc'), 1, 18)
    )

    if (not Lib.IsDigits([aPage, aLimit])):
        return {'status_code': 404}

    aLangId = self.GetLangId(aLang)
    aLimit = min(aLimit, 50)
    await self.Lang.Add(aLang, 'product/category')

    aSearch = aSearch.replace('_', ' ')
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

    SessionId = Lib.DeepGetByList(aData, ['session', 'session_id'])
    if (SessionId):
        await self.ExecModel(
            'ref_product/product',
            {
                'method': 'Ins_HistProductSearch',
                'param': {
                    'aText': aSearch,
                    'aResults': Found,
                    'aLangId': aLangId,
                    'aSessionId': SessionId
                }
            }
        )

    if (Found):
        if (self.ApiCtrl.Conf.get('seo_url')):
            Href = await Lib.SeoEncodeStr(self, Lib.UrlEncode(aData['query']))
        else:
            Href = aData['path_qs']

        Pagination = Lib.TPagination(aLimit, Href)
        PData = Pagination.Get(Dbl.Rec.total, aPage)
        DblPagination = Lib.TDbList(['page', 'title', 'href', 'current'], PData)

        DblProducts = await products_a(self, Dbl)
        Title = f"{Lib.ResGetLang(aData, 'found')} {Found}. {Lib.ResGetLang(aData, 'page')} {aPage}"

        dbl_products_a_sort = GetProductsSort(Pagination.Href, f'&sort={aSort}&order={aOrder}', aData['res']['lang'])

        Res = {
            'dbl_products_a': DblProducts.Export(),
            'products_a_title': Title,
            'dbl_products_a_sort': dbl_products_a_sort.Export(),
            'dbl_pagenation': DblPagination.Export(),
            'found': Found,
            'search': aSearch
        }
    else:
        Res = {
            'found': Found,
            'search': aSearch
        }

    DictRepl = Lib.TDictReplDeep(Res)
    Res['meta_title'] = DictRepl.Parse(Lib.ResGetItem(aData, 'meta_title'))
    return Res
