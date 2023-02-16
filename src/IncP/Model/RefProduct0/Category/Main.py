# Created: 2023.01.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.UtilP.Db.DbModel import TDbModel


class TMain(TDbModel):
    async def GetCount(self):
        return 1
