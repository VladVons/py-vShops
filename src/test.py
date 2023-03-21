# Created: 2023.03.19
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import asyncio
import time
import random
#
from Inc.Misc.Cache import TCacheFile


async def Main():
    Cnt = 0
    #Cache = TCacheMem('', 10)
    Cache = TCacheFile('Data/cache/temp', 10)

    for i in range(20):
        Query = {'key1': 1, 'key2': random.randint(0, 5)}
        Data = Cache.Get('common/home', Query)
        if (not Data):
            Cache.Set('common/home', Query, f'Time is {time.time()}')
            Cnt += 1
        time.sleep(0.5)
        print(i, Cnt)


    print('done')

asyncio.run(Main())
print('done')
