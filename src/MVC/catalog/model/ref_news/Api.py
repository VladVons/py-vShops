# Created: 2024.03.13
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


async def Get_Item(self, aLangId: int, aNewsId: int) -> dict:
    return await self.ExecQuery(
        'fmtGet_Item.sql',
        {'aLangId': aLangId, 'aNewsId': aNewsId}
    )

async def Get_List(self, aLangId: int, aGroupId: int, aLimit: int, aOffset: int) -> dict:
    return await self.ExecQuery(
        'fmtGet_List.sql',
        {'aLangId': aLangId, 'aGroupId': aGroupId, 'aLimit': aLimit, 'aOffset': aOffset}
    )
