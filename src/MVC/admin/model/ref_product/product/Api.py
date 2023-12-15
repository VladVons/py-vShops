# Created: 2023.12.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


async def Get_Product_LangId(self, aLangId: int, aTenantId: int, aProductId: int) -> dict:
    return await self.ExecQuery(
        'fmtGet_Product_LangId.sql',
        {'aLangId': aLangId, 'aTenantId': aTenantId, 'aProductId': aProductId}
    )
