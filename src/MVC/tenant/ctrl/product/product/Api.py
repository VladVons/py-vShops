# Created: 2023.12.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
#
from Inc.Util.Obj import DeepGetByList
from IncP.LibCtrl import GetDictDefs


async def Save(self, aPost: dict, aLangId: int, aTenantId: int, aProductId: int) -> dict:
    Changes = json.loads(aPost['changes'])
    Dbl = await self.ExecModelImport(
        'ref_product/product',
        {
            'method': 'Set_Product',
            'param': {'aLangId': aLangId, 'aTenantId': aTenantId, 'aProductId': aProductId, 'aChanges': Changes}
        }
    )
    pass

async def Main(self, aData: dict = None) -> dict:
    aLang, aProductId = GetDictDefs(
        aData.get('query'),
        ('lang', 'product_id'),
        ('ua', 0)
    )

    aLangId = self.GetLangId(aLang)
    AuthId = DeepGetByList(aData, ['session', 'auth_id'])

    if (aData['post']):
        await Save(self, aData['post'], aLangId, AuthId, aProductId)

    DblProduct = await self.ExecModelImport(
        'ref_product/product',
        {
            'method': 'Get_Product_LangId',
            'param': {'aLangId': aLangId, 'aTenantId': AuthId, 'aProductId': aProductId}
        }
    )
    if (DblProduct):
        return {
            'product': DblProduct.Rec.GetAsDict()
        }
