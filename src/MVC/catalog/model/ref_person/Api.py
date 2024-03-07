# Created: 2023.08.13
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


async def Get_PersonPhoneName (self, aPhone: str, aFirstName: str) -> dict:
    return await self.ExecQuery(
        'fmtGet_PersonPhoneName.sql',
        {'aPhone': aPhone, 'aFirstName': aFirstName}
    )

async def Set_PersonPhoneName (self, aPhone: str, aFirstName: str, aLastName: str, aMiddleName: str) -> dict:
    return await self.ExecQuery(
        'fmtSet_PersonPhoneName.sql',
        {'aPhone': aPhone, 'aFirstName': aFirstName, 'aLastName': aLastName, 'aMiddleName': aMiddleName}
    )
