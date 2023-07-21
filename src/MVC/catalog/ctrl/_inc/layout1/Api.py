# Created: 2023.07.17
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.DictDef import TDictKey


async def Main(self, aData: dict = None) -> dict:
    Urls = {
        'cart': '?route=checkout/cart',
        'order': '?route=checkout/order',
        'history': '?route=checkout/history',
        'contact': '?route=information/contact',
        'compare': '?api=information/compare'
    }

    Res = {'url': TDictKey('', Urls)}
    return Res
