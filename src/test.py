# Created: 2023.03.19
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import asyncio
import time
#
from IncP.ViewCache import TViewCache

async def Main():
    ViewCache = TViewCache('Cache/view', 30)
    Data = ViewCache.Get('common/home', {'key1': 1, 'key2': 2})
    if (not Data):
        ViewCache.Set('common/home', {'key1': 1, 'key2': 2}, f'Time is {time.time()}')

    print('done')

asyncio.run(Main())
print('done')
