# Created: 2023.08.13
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Sql import ListsToComma


async def Add_OrderMix(self, aCustomerId: int, aRows: list) -> dict:
    Products = ListsToComma(aRows)
    return await self.ExecQuery(
        'fmtAdd_OrderMix.sql',
        {'aCustomerId': aCustomerId, 'Rows': Products}
    )
