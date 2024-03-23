# Created: 2023.08.13
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Sql import ListsToComma


async def Add_OrderMix(self, aPersonId: int, aRows: list) -> dict:
    Products = ListsToComma(aRows)
    return await self.ExecQuery(
        'fmtAdd_OrderMix.sql',
        {'aPersonId': aPersonId, 'Rows': Products}
    )

async def Get_OrderMix(self, aOrderId: int) -> dict:
    return await self.ExecQuery(
        'fmtGet_OrderMix.sql',
        {'aOrderId': aOrderId}
    )

async def Get_OrderMixTableProduct(self, aOrderId: int, aLangId: int) -> dict:
    return await self.ExecQuery(
        'fmtGet_OrderMixTableProduct.sql',
        {'aOrderId': aOrderId, 'aLangId': aLangId}
    )

async def Get_OrdersMix(self, aPersonId: int) -> dict:
    return await self.ExecQuery(
        'fmtGet_OrdersMix.sql',
        {'aPersonId': aPersonId}
    )
