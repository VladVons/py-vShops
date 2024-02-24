# Created: 2024.02.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import DeepGetByList


async def Main(self, aData: dict) -> dict:
    AuthId = DeepGetByList(aData, ['session', 'auth_id'])

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
