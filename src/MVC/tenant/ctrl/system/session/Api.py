# Created: 2023.12.11
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib


async def RegSession(self, aData: dict) -> dict:
    return await self.ExecModel('system', Lib.Filter(aData, ['method', 'param']))

async def OnExec(self, aData: dict) -> dict:
    pass
