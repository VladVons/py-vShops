# Created: 2024.03.13
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


async def Get_News(self, aLangId: int, aNewsId: int) -> dict:
    return await self.ExecQuery(
        'fmtGet_News.sql',
        {'aLangId': aLangId, 'aNewsId': aNewsId}
    )
