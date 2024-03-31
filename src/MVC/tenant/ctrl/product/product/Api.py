# Created: 2023.12.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
#
import IncP.LibCtrl as Lib


async def ajax(self, aData: dict = None) -> dict:
    aLang = aData.get('lang', 'ua')
    LangId = self.GetLangId(aLang)
    AuthId = Lib.DeepGetByList(aData, ['session', 'auth_id'])
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
    aLang, aProductId = Lib.GetDictDefs(
        aData.get('query'),
        ('lang', 'product_id'),
        ('ua', 0)
    )

    aLangId = self.GetLangId(aLang)
    AuthId = Lib.DeepGetByList(aData, ['session', 'auth_id'])

    Post = aData.get('post')
    if (Post and len(Post.get('changes', '')) > 2):
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
        DblPrice = await self.ExecModelImport(
            'ref_product/price',
            {
                'method': 'Get_PriceHist_Product',
                'param': {'aProductId': aProductId}
            }
        )
        ProductPriceHist = DblPrice.Export()

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
        if (not DblImages):
            DblImages = Lib.TDbList(['name', 'type', 'size', 'date', 'href', 'path', 'sort_order', 'enabled', 'image'])
        # add extra new blank record
        DblImages.RecAdd().SetAsDict({
            'name': '', 'size': -1, 'date': 0, 'href': '', 'path': '', 'sort_order': 0, 'enabled': False, 'image': ''
        })

        DblImages0 = None
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

            DblImages0 = await self.GetImages0(DblProduct.Rec.product0_id)

        Res = {
            'product': DblProduct.Rec.GetAsDict() | {'price_hist': ProductPriceHist},
            'product0': DblProduct0 and DblProduct0.Rec.GetAsDict(),
            'dbl_images': DblImages and DblImages.Export(),
            'dbl_images0': DblImages0 and DblImages0.Export(),
            'href': {
                'category_ajax': f'/{self.Name}/api/?route=product/product'
            }
        }

        #await self.Lang.Add(aLang, 'common/filemanager')
        #ResCF = await self.ExecSelf('common/filemanager', aData)
        #ResAll = DictUpdateDeep(Res, ResCF, True)
        return Res
    pass