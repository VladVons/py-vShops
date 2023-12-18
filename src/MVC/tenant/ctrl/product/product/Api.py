# Created: 2023.12.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Obj import DeepGetByList
from IncP.LibCtrl import GetDictDefs


async def Main(self, aData: dict = None) -> dict:
    aLang, aProductId = GetDictDefs(
        aData.get('query'),
        ('lang', 'product_id'),
        ('ua', 0)
    )
    aLangId = self.GetLangId(aLang)
    AuthId = DeepGetByList(aData, ['session', 'auth_id'])

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
