# Created: 2023.10.26
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from ..._inc.products_a import Main as products_a


async def Main(self, _aData: dict = None) -> dict:
    LangId = self.GetLangId('ua')
    Dbl = await self.ExecModelImport(
        'ref_product0/product',
        {
            'method': 'Get_ProductsRnd_LangImagePrice',
            'param': {
                'aLangId': LangId,
                'aLimit': 12
            }
        }
    )
    if (Dbl):
        Dbl = await products_a(self, Dbl)
        return {
            'dbl_products_a': Dbl.Export()
        }
