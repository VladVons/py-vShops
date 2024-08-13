# Created: 2023.02.22
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibModel as Lib

async def Ins_HistProductSearch(self, aLangId: int, aSessionId: int, aText: str, aResults: int):
    MaxLen = 64
    await self.ExecQuery(
        'fmtIns_HistProductSearch.sql',
        {
            'aLangId': aLangId,
            'aSessionId': aSessionId,
            'aText': Lib.Escape(aText[:MaxLen]),
            'aResults': aResults
        }
    )

async def Ins_HistProductView(self, aProductId: int, aSessionId: int):
    await self.ExecQuery(
        'fmtIns_HistProductView.sql',
        {'aProductId': aProductId, 'aSessionId': aSessionId}
    )
