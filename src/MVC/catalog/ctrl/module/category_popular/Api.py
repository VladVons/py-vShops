# Created: 2024.05.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib


async def Main(self, aData: dict = None) -> dict:
    aLang = Lib.DeepGetByList(aData, ['query', 'lang'], 'ua')
    aLangId = self.GetLangId(aLang)

    Dbl = await self.ExecModelImport(
        'ref_product0/category',
        {
            'method': 'Get_CategoryPopular',
            'param': {
                'aLangId': aLangId
            }
        }
    )

    if (Dbl):
        pass
