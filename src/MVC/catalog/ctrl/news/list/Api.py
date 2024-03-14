# Created: 2024.03.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import GetDictDefs, IsDigits


async def Main(self, aData: dict = None) -> dict:
    aLang, aPage, aLimit = GetDictDefs(
        aData.get('query'),
        ('lang', 'page', 'limit'),
        ('ua', 1, 20)
    )

    if (not IsDigits([aPage, aLimit])):
        return {'err_code': 404}

    aLimit = max(aLimit, 50)
    aLangId = self.GetLangId(aLang)
    Dbl = await self.ExecModelImport(
        'ref_news',
        {
            'method': 'Get_List',
            'param': {
                'aLangId': aLangId,
                'aLimit': aLimit,
                'aOffset': (aPage - 1) * aLimit
            }
        }
    )
    if (not Dbl):
        return {'err_code': 404}

    return {
        'dbl_news': Dbl.Export()
    }
