# Created: 2024.02.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


async def Get_ModelUnknown(self, aTenantId: int) -> dict:
    return await self.ExecQuery(
        'fmtGet_ModelUnknown.sql',
        {'aTenantId': aTenantId}
    )
