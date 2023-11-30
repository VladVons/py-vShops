# Created: 2023.10.26
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import GetDictDef, TDbSql
from ..._inc.products_a import Main as products_a


async def Main(self, aData: dict = None) -> dict:
    aLang, = GetDictDef(
        aData.get('query'),
        ('lang',),
        ('ua',)
    )

    Dbl = await self.ExecModelImport(
        'ref_product0/product',
        {
            'method': 'Get_ProductsRnd_LangImagePrice',
            'param': {'aLangId': self.GetLangId(aLang), 'aLimit': 12}
        }
    )
    if (not Dbl):
        return

    Dbl = await products_a(self, Dbl)
    return {'dbl_products_a': Dbl.Export()}
