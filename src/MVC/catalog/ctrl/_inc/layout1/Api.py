# Created: 2023.07.17
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


async def Main(self, _aData: dict = None) -> dict:
    Dbl = await self.ExecModelImport (
        'ref_product0/category',
        {
            'method': 'Get_CategoriesSubCount_ParentLang',
            'param': {
                'aLang': 'ua',
                'aParentIdRoot': 0
            }
        }
    )
    if (not Dbl):
        return

    Categories = {}
    for Rec in Dbl:
        ParentId = Dbl.Rec.parent_id
        if (ParentId not in Categories):
            Categories[ParentId] = []
        Data = Rec.GetAsDict() | {'href': f'?route=product0/category&category_id={Rec.id}'}
        Categories[ParentId].append(Data)

    Href = {
        'about_us': '/?route=information/about_us',
        'contacts': '/?route=information/contacts',
        'history': '/?route=checkout/history',
        'order': '/?route=checkout/order',
        'search': '/?route=product0/search&q=',
        'search_ajax': '/api/?route=product0/search'
    }

    return {
        'categories_a': Categories, 'id_a': 0,
        'href_layout': Href
    }
