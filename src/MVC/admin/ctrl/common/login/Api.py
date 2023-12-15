# Created: 2023.12.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import GetDictDefs


async def Main(self, aData: dict = None) -> dict:
    aUser, aPassw = GetDictDefs(
        aData.get('post'),
        ('user', 'password'),
        ('', '')
    )

    if (aUser):
        Dbl = await self.ExecModelImport(
            'system',
            {
                'method': 'Get_TenantAuth',
                'param': {'aAlias': aUser, 'aPasswd': aPassw}
            }
        )
        if (Dbl):
            return {'type': 'tenant', 'id': Dbl.Rec.id}
