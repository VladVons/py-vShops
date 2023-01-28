# Created: 2023.01.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Mod import Decor_AddModules
from Inc.UtilP.Db.DbModel import TDbModel
from . import MainGet


@Decor_AddModules([MainGet])
class TMain(TDbModel):
    Text = 'Pink'

    async def GetCount(self):
        return 1
