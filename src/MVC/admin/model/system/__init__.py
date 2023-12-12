# Created: 2023.02.16
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Mod import DAddModules, DAddFiles
from Inc.Sql.DbModel import TDbModel
from . import Api


@DAddModules([Api], '*')
#@DAddFiles(__name__, 'Api.*', '*')
class TMain(TDbModel):
    pass
