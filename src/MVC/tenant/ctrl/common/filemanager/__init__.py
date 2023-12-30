# Created: 2023.12.29
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Mod import DAddModules
from IncP.CtrlBase import TCtrlBase
from IncP.LibCtrl import TDbSql
from . import Api


@DAddModules([Api], '*')
class TMain(TCtrlBase):
    pass
