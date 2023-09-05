# Created: 2023.08.13
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

async def Get_CustomerPhoneName (self, aPhone: str, aFirstName: str) -> dict:
    return await self.ExecQuery(
        'fmtGet_CustomerPhoneName.sql',
        {'aPhone': aPhone, 'aFirstName': aFirstName}
    )

async def Set_CustomerPhoneName (self, aPhone: str, aFirstName: str) -> dict:
    return await self.ExecQuery(
        'fmtSet_CustomerPhoneName.sql',
        {'aPhone': aPhone, 'aFirstName': aFirstName}
    )
