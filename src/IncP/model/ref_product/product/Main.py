# Created: 2023.01.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Mod import DAddModules
from Inc.Sql.DbModel import TDbModel
from Inc.Sql.DbMeta import TDbMeta
from . import Sql, Api


@DAddModules([Sql, Api], True)
class TMain(TDbModel):
    def __init__(self, aDbMeta: TDbMeta, aPath: str):
        super().__init__(aDbMeta, aPath)