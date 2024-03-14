# Created: 2023.02.28
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


async def Get_AttrAlias(self, aLangId: int, aAlias: str) -> dict:
    return await self.ExecQuery(
        'fmtGet_AttrAlias.sql',
        {'aLangId': aLangId, 'aAlias': aAlias}
    )

async def Get_AttrFilter(self) -> dict:
    return await self.ExecQuery(
        'fmtGet_AttrFilter.sql',
        {}
    )
