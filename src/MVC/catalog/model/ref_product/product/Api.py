# Created: 2023.02.22
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


async def Ins_HistProductSearch(self, aLangId: int, aSessionId: int, aText: str, aResults: int):
    await self.ExecQuery(
        'fmtIns_HistProductSearch.sql',
        {'aLangId': aLangId, 'aSessionId': aSessionId, 'aText': aText[:64], 'aResults': aResults}
    )

async def Ins_HistProductView(self, aProductId: int, aSessionId: int):
    await self.ExecQuery(
        'fmtIns_HistProductView.sql',
        {'aProductId': aProductId, 'aSessionId': aSessionId}
    )
