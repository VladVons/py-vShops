# Created: 2023.01.20
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Plugin import TPlugin
from Inc.Sql.DbMeta import TDbMeta


class TPlugins(TPlugin):
    def _Create(self, aModule: object, aPath: str) -> object:
        Res = aModule.TMain(self.DbMeta, self.Dir + '/' + aPath)
        return Res

class TModels(TPlugins):
    def __init__(self, aDir: str, aDbMeta: TDbMeta):
        super().__init__(aDir)
        self.DbMeta = aDbMeta

class TCtrls(TPlugins):
    pass

class TViewes(TPlugins):
    pass
