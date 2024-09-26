# Created: 2023.07.29
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Mod import DAddFiles
from IncP.CtrlBase import TCtrlBase
from . import Api


@DAddFiles(__name__, 'Api.*', 'Api')
class TMain(TCtrlBase):
    pass
