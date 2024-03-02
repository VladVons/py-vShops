# Created: 2023.03.08
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Mod import DAddModules
from IncP.CtrlBase import TCtrlBase
from . import Api


@DAddModules([Api], '*')
class TMain(TCtrlBase):
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
