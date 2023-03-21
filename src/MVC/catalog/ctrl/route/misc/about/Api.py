# Created: 2023.03.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


async def Main(self, _aQuery: dict = None) -> dict:
    Res = await self.ExecModel('system', {"method": "GetDbInfo"})
    return Res
