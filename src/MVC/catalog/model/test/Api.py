# Created: 2024.03.11
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


async def Get_HistSession(self, aLimit: int, aOffset: int) -> dict:
    return await self.ExecQuery(
        'fmtGet_HistSession.sql',
        {'aLimit': aLimit, 'aOffset': aOffset}
    )
