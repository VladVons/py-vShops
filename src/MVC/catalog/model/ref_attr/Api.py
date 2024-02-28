# Created: 2023.02.28
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


async def Get_PriceHist_ProductDate(self, aLangId: int, aAlias: str) -> dict:
    return await self.ExecQuery(
        'fmtGet_AttrAlias.sql',
        {'aLangId': aLangId, 'aAlias': aAlias}
    )
