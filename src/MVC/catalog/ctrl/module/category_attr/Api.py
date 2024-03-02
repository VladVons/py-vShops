# Created: 2024.03.02
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


async def Main(self, _aData: dict = None) -> dict:
    LangId = self.GetLangId('ua')
    Dbl = await self.ExecModelImport(
        'ref_product0/category',
        {
            'method': 'Get_CategoryAttr',
            'param': {
                'aLangId': LangId,
                'aCategoryId': 4
            }
        }
    )
    if (Dbl):
        return {
            'dbl_category_attr': Dbl.Export()
        }
