# Created: 2023.02.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Sql.ADb import ListIntToComma


async def GetProductsImages(self, aProductIds: list[int]) -> dict:
    ProductIds = ListIntToComma(aProductIds)
    return await self.ExecQuery(
        'fmtGetProductsImages.sql',
        {'ProductIds': ProductIds}
    )

async def GetProductsWithoutImages(self, aTenantId: int) -> dict:
    return await self.ExecQuery(
        'fmtGetProductsWithoutImages.sql',
        {'aTenantId': aTenantId}
    )

async def GetProductsCountImages(self, aTenantId: int) -> dict:
    return await self.ExecQuery(
        'fmtGetProductsCountImages.sql',
        {'aTenantId': aTenantId}
    )
