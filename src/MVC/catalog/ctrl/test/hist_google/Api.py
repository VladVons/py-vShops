# Created: 2024.04.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib


async def Main(self, aData: dict = None) -> dict:
    aPage, aLimit = Lib.GetDictDefs(
        aData.get('query'),
        ('page', 'limit'),
        (1, 50)
    )

    if (not Lib.IsDigits([aPage, aLimit])):
        return {'status_code': 404}

    Dbl = await self.ExecModelImport(
        'test',
        {
            'method': 'Get_HistGoogle',
            'param': {
                'aHost': aData['host'],
                'aLimit': aLimit,
                'aOffset': (aPage - 1) * aLimit
            }
        }
    )
    if (not Dbl):
        return

    Pagination = Lib.TPagination(aLimit, aData['path_qs'])
    PData = Pagination.Get(Dbl.Rec.total, aPage)
    DblPagination = Lib.TDbList(['page', 'title', 'href', 'current'], PData)

    return {
        'dbl': Dbl.Export(),
        'dbl_pagenation': DblPagination.Export()
    }
