# Created: 2024.03.29
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Mod import DAddModules, DAddFiles
from Inc.Sql.DbModel import TDbModel
from . import Api


@DAddModules([Api], '*')
class TMain(TDbModel):
    pass
