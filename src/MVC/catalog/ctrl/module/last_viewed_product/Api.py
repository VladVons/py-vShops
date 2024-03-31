# Created: 2024.02.25
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib
from ..._inc.products_a import Main as products_a


async def Main(self, aData: dict = None) -> dict:
    aLang = Lib.DeepGetByList(aData, ['query', 'lang'], 'ua')
    LangId = self.GetLangId(aLang)
    aSessionId = Lib.DeepGetByList(aData, ['session', 'session_id'])
    if (not aSessionId):
        return

    Dbl = await self.ExecModelImport(
        'ref_product0/product',
        {
            'method': 'Get_ProductsLastView_LangImagePrice',
            'param': {
                'aLangId': LangId,
                'aSessionId': aSessionId,
                'aLimit': 6
            }
        }
    )

    if (len(Dbl) > 0):
        DblProducts = await products_a(self, Dbl)
        return {
            'dbl_products_a': DblProducts.Export(),
            'products_a_title': Lib.ResGetLang(aData, 'viewed'),
        }
