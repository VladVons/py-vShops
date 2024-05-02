# Created: 2024.05.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Mod import DAddModules, DAddFiles
from IncP.CtrlBase import TCtrlBase
from . import Api


#@DAddModules([Api], '*')
@DAddFiles(__name__, 'Api.*', 'Api')
class TMain(TCtrlBase):
    pass
