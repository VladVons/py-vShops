# Created: 2024.03.02
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import GetDictDefs, IsDigits


async def Main(self, aData: dict = None) -> dict:
    aCategoryId, aLang = GetDictDefs(
        aData.get('query'),
        ('category_id', 'lang'),
        ('0', 'ua')
    )

    if (not IsDigits([aCategoryId])):
        return {'err_code': 404}

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
