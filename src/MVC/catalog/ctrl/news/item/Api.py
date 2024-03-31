# Created: 2024.03.13
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib


async def Main(self, aData: dict = None) -> dict:
    aLang, aNewsId = Lib.GetDictDefs(
        aData.get('query'),
        ('lang', 'news_id'),
        ('ua', 0)
    )

    aLangId = self.GetLangId(aLang)
    if (not Lib.IsDigits([aLangId, aNewsId])):
        return {'status_code': 404}


    Dbl = await self.ExecModelImport(
        'ref_news',
        {
            'method': 'Get_Item',
            'param': {
                'aLangId': aLangId,
                'aNewsId': aNewsId
            }
        }
    )
    if (not Dbl):
        return {'status_code': 404}

    Res = Dbl.Rec.GetAsDict()
    Res['descr'] = Res['descr'].replace('\n', '<br>')

    return Res
