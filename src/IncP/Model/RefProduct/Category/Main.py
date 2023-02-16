# Created: 2023.02.16
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Mod import DAddModules
from Inc.UtilP.Db.DbModel import TDbModel
from Inc.UtilP.Db.DbMeta import TDbMeta
from . import Sql, Get


@DAddModules([Sql], True)
class TMain(TDbModel):
    def __init__(self, aDbMeta: TDbMeta, aPath: str):
        super().__init__(aDbMeta, aPath)
