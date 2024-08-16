# Created: 2024.08.16
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib


async def Main(self, aData: dict = None) -> dict:
    aPage, aLimit = Lib.GetDictDefs(
        aData.get('query'),
        ('page', 'limit'),
        (1, 30)
    )

    if (not Lib.IsDigits([aPage, aLimit])):
        return {'status_code': 404}

    #Host = aData['host']
    Host = '1x1.com.ua'

    DblDay = await self.ExecModelImport(
        'test',
        {
            'method': 'Get_HistUniqIpPerDay',
            'param': {
                'aHost': Host,
                'aLimit': aLimit,
                'aOffset': (aPage - 1) * aLimit
            }
        }
    )

    Pagination = Lib.TPagination(aLimit, aData['path_qs'])
    PData = Pagination.Get(DblDay.Rec.total, aPage)
    DblPagination = Lib.TDbList(['page', 'title', 'href', 'current'], PData)

    Res = {
        'dbl_pagenation': DblPagination.Export(),
        'dbl_day': DblDay.Export()
    }
    return Res
