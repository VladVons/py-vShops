# Created: 2024.03.02
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import GetDictDefs


async def Main(self, aData: dict = None) -> dict:
    aCategoryId, aLang = GetDictDefs(
        aData.get('query'),
        ('category_id', 'lang'),
        ('0', 'ua')
    )
    aLangId = self.GetLangId(aLang)

    Dbl = await self.ExecModelImport(
        'ref_product0/category',
        {
            'method': 'Get_CategoryAttr',
            'param': {
                'aLangId': aLangId,
                'aCategoryId': aCategoryId
            }
        }
    )
    if (Dbl):
        return {
            'dbl_category_attr': Dbl.Export()
        }
