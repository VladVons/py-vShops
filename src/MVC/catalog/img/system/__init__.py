# Created: 2023.04.18
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Mod import DAddModules
from IncP.ImgBase import TImgBase
from . import Api


@DAddModules([Api], '*')
class TMain(TImgBase):
    pass
