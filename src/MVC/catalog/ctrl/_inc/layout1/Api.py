# Created: 2023.07.17
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import GetDictDefs, SeoEncodeDict

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
            Data = Rec.GetAsDict() | {'href': f'/?route=product0/category&category_id={Rec.id}'}
            Res[ParentId].append(Data)
    return Res

async def ajax(self, aData: dict = None) -> dict:
    aLang = aData.get('lang', 'ua')
    LangId = self.GetLangId(aLang)
    return await GetCategories(self, LangId)

async def Main(self, aData: dict = None) -> dict:
    aSearch, _aLang = GetDictDefs(
        aData.get('query'),
        ('q', 'lang'),
        ('', 'ua')
    )

    Href = {
        'about_us': '/?route=info/about_us',
        'contacts': '/?route=info/contacts',
        'faq': '/?route=info/faq',
        'news': '/?route=news/list',
        'privacy_policy': '/?route=info/privacy_policy',
        'sitemap': '/?route=info/sitemap',

        'order': '/?route=checkout/order',
        'payment': '/?route=checkout/payment',
        'search': '/?route=product0/search&q=',
        'login_tenant': '/tenant/?route=common/login',
        'search_ajax': '/api/?route=product0/search',
        'category_ajax': '/api/?route=_inc/layout1'
    }
    Href = await SeoEncodeDict(self, Href)

    Res = {
        'href': Href,
        'search': aSearch
    }

    return Res