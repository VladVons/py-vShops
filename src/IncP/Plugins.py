# Created: 2023.01.20
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Plugin import TPlugin
from Inc.Sql.DbMeta import TDbMeta


class TModels(TPlugin):
    def __init__(self, aDir: str, aDbMeta: TDbMeta):
        super().__init__(aDir)
        self.DbMeta = aDbMeta

    def _Create(self, aModule: object, aPath: str) -> object:
        Res = aModule.TMain(self.DbMeta, self.Dir + '/' + aPath)
        return Res

class TCtrls(TPlugin):
    def _Create(self, aModule: object, aPath: str) -> object:
        return aModule

class TViewes(TPlugin):
    def _Create(self, aModule: object, aPath: str) -> object:
        return aModule
