# Created: 2024.03.11
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib


async def Main(self, aData: dict = None) -> dict:
    aPage, aLimit, aHaving = Lib.GetDictDefs(
        aData.get('query'),
        ('page', 'limit', 'having'),
        (1, 50, 0)
    )

    if (not Lib.IsDigits([aPage, aLimit, aHaving])):
        return {'status_code': 404}

    Host = aData['host']
    Host = '1x1.com.ua'

    DblMain = await self.ExecModelImport(
        'test',
        {
            'method': 'Get_HistSession',
            'param': {
                'aHost': Host,
                'aLimit': aLimit,
                'aOffset': (aPage - 1) * aLimit,
                'aHaving': aHaving
            }
        }
    )
    if (not DblMain):
        return

    Href = aData['path_qs']
    #Href = UrlEncode(aData['query'])

    Pagination = Lib.TPagination(aLimit, Href)
    PData = Pagination.Get(DblMain.Rec.total, aPage)
    DblPagination = Lib.TDbList(['page', 'title', 'href', 'current'], PData)

    DblDay = await self.ExecModelImport(
        'test',
        {
            'method': 'Get_HistUniqIpPerDay',
            'param': {
                'aHost': Host
            }
        }
    )

    Res = {
        'dbl_main': DblMain.Export(),
        'dbl_pagenation': DblPagination.Export(),
        'day_inf': DblDay.ExportPairs('create_day', ['count', 'count_id', 'count_url', 'count_ip', 'count_location'], True)
    }
    return Res
