# Created: 2023.12.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib


async def Main(self, aData: dict = None) -> dict:
    aSearch, _aLang = Lib.GetDictDefs(
        aData.get('query'),
        ('q', 'lang'),
        ('', 'ua')
    )

    return {
        'href': {
            'faq': f'/{self.Name}/?route=info/faq',
            'products': f'/{self.Name}/?route=product/products',
            'filemanager2': f'/{self.Name}/?route=common/filemanager2',
            'price_list_import': f'/{self.Name}/?route=misc/price_list_import',
            'model_unknown': f'/{self.Name}/?route=test/model_unknown',

            'search_ajax': '/api/?route=product0/search',
            'category_ajax': f'/{self.Name}/api/?route=product/product'
        },
        'search': aSearch
    }
