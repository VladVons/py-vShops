# Created: 2024.02.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib


async def Main(self, aData: dict) -> dict:
    AuthId = Lib.DeepGetByList(aData, ['session', 'auth_id'])

    Dbl = await self.ExecModelImport(
        'test',
        {
            'method': 'Get_ModelUnknown',
            'param': {
                'aTenantId': AuthId,
            }
        }
    )

    return {'dbl_model_unknown': Dbl.Export()}
