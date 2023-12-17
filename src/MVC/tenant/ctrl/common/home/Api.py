# Created: 2023.12.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from Inc.Util.Obj import DeepGetByList
from IncP.LibCtrl import GetDictDefs



async def Main(self, aData: dict = None) -> dict:
    AuthId = DeepGetByList(aData, ['session', 'auth_id'])
    Dbl = await self.ExecModelImport(
        'ref_product/product',
        {
            'method': 'Get_ProductsStat',
            'param': {'aTenantId': AuthId}
        }
    )
    return {'product_inf': Dbl.Rec.GetAsDict()}
