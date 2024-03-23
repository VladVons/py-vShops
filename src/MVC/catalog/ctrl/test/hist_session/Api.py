# Created: 2024.03.11
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import GetDictDefs, IsDigits, TPagination, TDbList


async def Main(self, aData: dict = None) -> dict:
    aPage, aLimit, aHaving = GetDictDefs(
        aData.get('query'),
        ('page', 'limit', 'having'),
        (1, 50, 0)
    )

    if (not IsDigits([aPage, aLimit, aHaving])):
        return {'status_code': 404}

    Dbl = await self.ExecModelImport(
        'test',
        {
            'method': 'Get_HistSession',
            'param': {
                'aHost': aData['host'],
                'aLimit': aLimit,
                'aOffset': (aPage - 1) * aLimit,
                'aHaving': aHaving
            }
        }
    )
    if (not Dbl):
        return {'status_code': 404}

    Pagination = TPagination(aLimit, aData['path_qs'])
    PData = Pagination.Get(Dbl.Rec.total, aPage)
    DblPagination = TDbList(['page', 'title', 'href', 'current'], PData)

    return {
        'dbl': Dbl.Export(),
        'dbl_pagenation': DblPagination.Export()
    }
