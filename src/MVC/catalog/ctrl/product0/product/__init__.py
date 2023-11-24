# Created: 2023.03.08
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Mod import DAddModules
from IncP.CtrlBase import TCtrlBase
from IncP.LibCtrl import TDbSql
from . import Api


@DAddModules([Api], '*')
class TMain(TCtrlBase):
    async def GetBreadcrumbs(self, aLang: str, aCategoryId: int) -> list:
        Res = []
        if (aCategoryId):
            Dbl = await self.ExecModelImport(
                'ref_product0/category',
                {
                    'method': 'Get_CategoryId_Path',
                    'param': {'aLang': aLang, 'aCategoryIds': [aCategoryId]}
                }
            )

            if (Dbl):
                for Title, Id in zip(Dbl.Rec.path_title, Dbl.Rec.path_id):
                    Res.append({'href': f'?route=product0/category&category_id={Id}', 'title': Title})
        return Res

    async def GetImages(self, aImages: list[str]) -> dict:
        Res = {'image': '/default/assets/img/no-image.png', 'images': []}
        if (aImages):
            Images = [f'product/{x}' for x in aImages]
            ResEI = await self.ExecImg(
                'system',
                {
                    'method': 'GetImages',
                    'param': {'aFiles': Images}
                }
            )

            Images = ResEI['image']
            if (Images):
                Res = {'image': Images[0], 'images': Images}
        return Res
