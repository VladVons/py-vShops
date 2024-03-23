# Created: 2024.03.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import GetDictDefs, IsDigits, TPagination, TDbList


async def Main(self, aData: dict = None) -> dict:
    aLang, aPage, aLimit = GetDictDefs(
        aData.get('query'),
        ('lang', 'page', 'limit'),
        ('ua', 1, 20)
    )

    if (not IsDigits([aPage, aLimit])):
        return {'status_code': 404}

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
        return {'status_code': 404}

    Pagination = TPagination(aLimit, aData['path_qs'])
    PData = Pagination.Get(Dbl.Rec.total, aPage)
    DblPagination = TDbList(['page', 'title', 'href', 'current'], PData)

    Dbl.AddFieldsFill(['href'], False)
    for Rec in Dbl:
        New = [f'/?route=news/item&news_id={Rec.id}']
        Dbl.RecMerge(New)

    return {
        'dbl_news': Dbl.Export(),
        'dbl_pagenation': DblPagination.Export()
    }
