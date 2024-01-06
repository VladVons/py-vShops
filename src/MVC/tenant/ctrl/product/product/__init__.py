# Created: 2023.12.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Mod import DAddModules
from IncP.CtrlBase import TCtrlBase
from IncP.LibCtrl import TDbList
from . import Api


@DAddModules([Api], '*')
class TMain(TCtrlBase):
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

    async def GetImages(self, aProductId: int) -> TDbList:
        DblDb = await self.ExecModelImport(
            'ref_product/product',
            {
                'method': 'Get_Product_Images',
                'param': {'aProductId': aProductId}
            }
        )

        if (DblDb and len(DblDb) > 0):
            Images = [f'product/{Rec.image}' for Rec in DblDb]
            DblData = await self.ExecImg(
                'system',
                {
                    'method': 'GetImagesInfo',
                    'param': {'aFiles': Images}
                }
            )
            DblImg = TDbList().Import(DblData)
            DblImg.MergeDbl(DblDb, ['sort_order', 'enabled'])
            return DblImg
