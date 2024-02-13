# Created: 2024.02.13
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Mod import DAddModules
from Inc.Sql.DbModel import TDbModel
from . import Api


@DAddModules([Api], '*')
class TMain(TDbModel):
    pass
