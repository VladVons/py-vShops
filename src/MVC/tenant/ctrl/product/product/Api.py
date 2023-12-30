# Created: 2023.12.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import DeepGetByList, GetDictDefs


async def GetCategories(self, aLangId: int, aTenantId: int) -> dict:
    Dbl = await self.ExecModelImport (
        'ref_product/category',
        {
            'method': 'Get_CategoriesSubCount_ParentLang',
            'param': {
                'aLangId': aLangId,
                'aTenantId': aTenantId,
                'aParentIdtRoot': 0
            }
        }
    )

    Res = {}
    if (Dbl):
        for Rec in Dbl:
            ParentIdt = Dbl.Rec.parent_idt
            if (ParentIdt not in Res):
                Res[ParentIdt] = []
            Data = Rec.GetAsDict() | {'href': '#', 'data': f'''onclick="OnClickCategory({Rec.id}, '{Rec.title}')"'''}
            Res[ParentIdt].append(Data)
    return Res

async def ajax(self, aData: dict = None) -> dict:
    aLang = aData.get('lang', 'ua')
    LangId = self.GetLangId(aLang)
    AuthId = DeepGetByList(aData, ['session', 'auth_id'])
    return await GetCategories(self, LangId, AuthId)


async def Save(self, aPost: dict, aLangId: int, aTenantId: int, aProductId: int) -> dict:
    await self.ExecModelImport(
        'ref_product/product',
        {
            'method': 'Set_Product',
            'param': {'aLangId': aLangId, 'aTenantId': aTenantId, 'aProductId': aProductId, 'aPost': aPost}
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
            'param': {'aLangId': aLangId, 'aTenantId': AuthId, 'aProductId': aProductId}
        }
    )
    if (DblProduct):
        DblCategory = await self.ExecModelImport(
            'ref_product/category',
            {
                'method': 'Get_CategoryId_Path',
                'param': {'aLangId': aLangId, 'aTenantId': AuthId, 'aCategoryIds': [DblProduct.Rec.category_id]}
            }
        )

        DblCategory.Rec.RenameFields(['id', 'path_title'], ['category_id', 'category_path'])
        DblProduct.MergeDbl(DblCategory, 'category_id', ['category_path'])
        return {
            'product': DblProduct.Rec.GetAsDict(),
            'href': {
                'category_ajax': '/tenant/api/?route=product/product'
            }
        }
