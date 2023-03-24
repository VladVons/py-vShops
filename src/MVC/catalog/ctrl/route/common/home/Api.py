# Created: 2023.03.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import time
from IncP.LibCtrl import TDbSql, GetDictDef


async def Main(self, aData: dict = None) -> dict:
    Res = {}
    #aTenantId, aLangId = GetDictDef(aData.get('query'), ('tenant', 'lang'), (2, 1))

    StartAt = time.time()
    Res['modules'] = await self.LoadModules(aData)
    print('---common/home', time.time() - StartAt)

    return Res
