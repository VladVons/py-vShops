# Created: 2023.12.11
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import Filter


async def RegSession(self, aData: dict) -> dict:
    return await self.ExecModel('system', Filter(aData, ['method', 'param']))

async def OnExec(self, aData: dict) -> dict:
    pass
