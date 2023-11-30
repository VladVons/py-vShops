# Created: 2023.07.17
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


async def GetCategories(self, aLangId: int) -> dict:
    Dbl = await self.ExecModelImport (
        'ref_product0/category',
        {
            'method': 'Get_CategoriesSubCount_ParentLang',
            'param': {
                'aLangId': aLangId,
                'aParentIdRoot': 0
            }
        }
    )

    Res = {}
    if (Dbl):
        for Rec in Dbl:
            ParentId = Dbl.Rec.parent_id
            if (ParentId not in Res):
                Res[ParentId] = []
            Data = Rec.GetAsDict() | {'href': f'?route=product0/category&category_id={Rec.id}'}
            Res[ParentId].append(Data)
    return Res

async def ajax(self, aData: dict = None) -> dict:
    aLang = aData.get('lang', 'ua')
    LangId = self.GetLangId(aLang)
    return await GetCategories(self, LangId)

async def Main(self, _aData: dict = None) -> dict:
    LangId = self.GetLangId('ua')
    Categories = await GetCategories(self, LangId)

    Href = {
        'about_us': '/?route=information/about_us',
        'contacts': '/?route=information/contacts',
        'history': '/?route=checkout/history',
        'order': '/?route=checkout/order',
        'search': '/?route=product0/search&q=',

        'search_ajax': '/api/?route=product0/search',
        'category_ajax': '/api/?route=_inc/layout1'
    }

    return {
        'categories_a': Categories, 'id_a': 0,
        'href_layout': Href
    }
