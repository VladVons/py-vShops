# Created: 2024.02.22
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib


async def Main(self, aData: dict = None) -> dict:
    AuthId = Lib.DeepGetByList(aData, ['session', 'auth_id'])

    Dbl = await self.ExecModelImport(
        'system',
        {
            'method': 'Get_TenantInf',
            'param': {
                'aTenantId': AuthId
            }
        }
    )

    return {'tenant': Dbl.Rec.GetAsDict()}
