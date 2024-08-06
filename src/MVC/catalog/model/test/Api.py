# Created: 2024.03.11
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


async def Get_HistSession(self, aHost: str, aLimit: int, aOffset: int, aHaving: int = 1) -> dict:
    #aHost = '1x1.com.ua'
    return await self.ExecQuery(
        'fmtGet_HistSession2.sql',
        {'aHost': aHost, 'aLimit': aLimit, 'aOffset': aOffset, 'aHaving': aHaving}
    )

async def Get_HistGoogle(self, aHost: str, aLimit: int, aOffset: int) -> dict:
    return await self.ExecQuery(
        'fmtGet_HistGoogle.sql',
        {'aHost': aHost, 'aLimit': aLimit, 'aOffset': aOffset}
    )
