# Created: 2023.03.11
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


async def RegSession(self, aData: dict) -> dict:
    return await self.ExecModel('system', aData.get('data'))
