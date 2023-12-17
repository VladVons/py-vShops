# Created: 2023.12.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import GetDictDefs


async def Main(self, aData: dict = None) -> dict:
    aUser, aPassword = GetDictDefs(
        aData.get('post'),
        ('user', 'password'),
        ('', '')
    )

    if (aUser):
        Dbl = await self.ExecModelImport(
            'system',
            {
                'method': 'Get_Auth',
                'param': {'aMailPhone': aUser, 'aPassword': aPassword}
            }
        )
        if (Dbl):
            if (Dbl.Rec.tenant_id):
                Id = Dbl.Rec.tenant_id
                Type = 'tenant'
            else:
                Id = Dbl.Rec.id
                Type = 'customer'
            return {'auth_path': Type, 'auth_id': Id}
