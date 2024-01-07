# Created: 2023.12.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
from IncP.LibCtrl import DeepGetByList, GetDictDefs


async def ajax(self, aData: dict = None) -> dict:
    aLang = aData.get('lang', 'ua')
    LangId = self.GetLangId(aLang)
    AuthId = DeepGetByList(aData, ['session', 'auth_id'])
    return await self.GetCategories(LangId, AuthId)

async def Save(self, aPost: dict, aLangId: int, aTenantId: int, aProductId: int) -> dict:
    await self.ExecModelImport(
        'ref_product/product',
        {
            'method': 'Set_Product',
            'param': {
                'aLangId': aLangId,
                'aTenantId': aTenantId,
                'aProductId': aProductId,
                'aPost': aPost
            }
        }
    )

async def Main(self, aData: dict = None) -> dict:
    aLang, aProductId = GetDictDefs(
        aData.get('query'),
        ('lang', 'product_id'),
        ('ua', 0)
    )

    aLangId = self.GetLangId(aLang)
    AuthId = DeepGetByList(aData, ['session', 'auth_id'])

    Post = aData.get('post')
    if (Post):
        await Save(self, Post, aLangId, AuthId, aProductId)

    DblProduct = await self.ExecModelImport(
        'ref_product/product',
        {
            'method': 'Get_Product_LangId',
            'param': {
                'aLangId': aLangId,
                'aTenantId': AuthId,
                'aProductId': aProductId
            }
        }
    )

    if (DblProduct):
        DblCategory = await self.ExecModelImport(
            'ref_product/category',
            {
                'method': 'Get_CategoryId_Path',
                'param': {
                    'aLangId': aLangId,
                    'aTenantId': AuthId,
                    'aCategoryIds': [DblProduct.Rec.category_id]
                }
            }
        )

        DblCategory.Rec.RenameFields(['id', 'path_title'], ['category_id', 'category_path'])
        DblProduct.MergeDblKey(DblCategory, 'category_id', ['category_path'])

        DblImages = await self.GetImages(aProductId)

        DblProduct0 = None
        if (DblProduct.Rec.product0_id):
            DblProduct0 = await self.ExecModelImport(
                'ref_product0/product',
                {
                    'method': 'Get_ProductInf_Id',
                    'param': {
                        'aLangId': aLangId,
                        'aId': DblProduct.Rec.product0_id
                    }
                }
            )

            DblProduct0.ToList()
            if (DblProduct0.Rec.features):
                AsStr = json.dumps(DblProduct0.Rec.features, indent=2, ensure_ascii=False)
                DblProduct0.Rec.features = AsStr

        Res = {
            'product': DblProduct.Rec.GetAsDict(),
            'product0': DblProduct0 and DblProduct0.Rec.GetAsDict(),
            'dbl_images': DblImages and DblImages.Export(),
            'href': {
                'category_ajax': '/tenant/api/?route=product/product'
            }
        }
        return Res
