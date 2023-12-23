# Created: 2023.12.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import GetDictDefs


async def Main(self, aData: dict = None) -> dict:
    aSearch, _aLang = GetDictDefs(
        aData.get('query'),
        ('q', 'lang'),
        ('', 'ua')
    )

    LangId = self.GetLangId('ua')

    Href = {
        'faq': f'/{self.Name}/?route=info/faq',
        'products': f'/{self.Name}/?route=product/products',
        'search_ajax': '/api/?route=product0/search',
        'category_ajax': '/tenant/api/?route=_inc/layout1'
    }

    return {
        'href_layout': Href,
        'search': aSearch
    }
