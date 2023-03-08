# Created: 2023.02.16
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Mod import DAddModules
from Inc.Sql import TDbModel
from . import Api


@DAddModules([Api], True)
class TMain(TDbModel):
    def __init__(self, aDbMeta, aPath):
        #super().__init__(aDbMeta, aPath)
        pass
