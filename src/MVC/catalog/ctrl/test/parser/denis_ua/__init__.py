# Created: 2024.04.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Mod import DAddModules
from IncP.CtrlBase import TCtrlBase
from . import Api


@DAddModules([Api], '*')
class TMain(TCtrlBase):
    pass
