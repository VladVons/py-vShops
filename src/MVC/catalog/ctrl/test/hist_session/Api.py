# Created: 2024.03.11
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import GetDictDefs, TPagination, TDbList


async def Main(self, aData: dict = None) -> dict:
    aPage, aLimit = GetDictDefs(
        aData.get('query'),
        ('page', 'limit'),
        (1, 50)
    )

    Dbl = await self.ExecModelImport(
        'test',
        {
            'method': 'Get_HistSession',
            'param': {
                'aLimit': aLimit,
                'aOffset': (aPage - 1) * aLimit
            }
        }
    )

    Pagination = TPagination(aLimit, aData['path_qs'])
    PData = Pagination.Get(Dbl.Rec.total, aPage)
    DblPagination = TDbList(['page', 'title', 'href', 'current'], PData)

    return {
        'dbl': Dbl.Export(),
        'dbl_pagenation': DblPagination.Export()
    }
