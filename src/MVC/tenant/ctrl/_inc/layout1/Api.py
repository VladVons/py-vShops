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

    return {
        'href_layout': {
            'faq': f'/{self.Name}/?route=info/faq',
            'products': f'/{self.Name}/?route=product/products',
            'filemanager': f'/{self.Name}/?route=common/filemanager',
            'search_ajax': '/api/?route=product0/search',
            'category_ajax': f'/{self.Name}/api/?route=product/product'
        },
        'search': aSearch
    }
