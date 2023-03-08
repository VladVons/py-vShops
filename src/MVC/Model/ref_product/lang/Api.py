# Created: 2023.02.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Sql.ADb import ListIntToComma


async def GetProductsIdForTenantAndLang(self, aTenantId: int, aLangId: int) -> dict:
    return await self.ExecQuery(
        'fmtGetProductsIdForTenantAndLang.sql',
        {'aTenantId': aTenantId, 'aLangId': aLangId}
    )

async def GetProductsLang(self, aProductIds: list[int], aLangId: id) -> dict:
    ProductIds = ListIntToComma(aProductIds)
    return await self.ExecQuery(
        'fmtGetProductsLang.sql',
        {'ProductIds': ProductIds, 'aLangId': aLangId}
    )

async def GetProductsWithoutLang(self, aTenantId: int, aLangId: int) -> dict:
    return await self.ExecQuery(
        'fmtGetProductsWithoutLang.sql',
        {'aTenantId': aTenantId, 'aLangId': aLangId}
    )
