# Created: 2023.01.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Mod import DAddModules
from Inc.UtilP.Db.DbModel import TDbModel
from . import Sql


@DAddModules([Sql])
class TMain(TDbModel):
    pass
