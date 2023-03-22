# Created: 2023.03.19
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import asyncio
import time
import random
import aiohttp
#
from Inc.Misc.Cache import TCacheFile

def Get(aModule, aQuery):
    print(f'{aModule}_{aQuery}')
    return ''

def Set(aModule, aQuery, aData):
    print(aData)

def Test2(aA1, aB1, aC1):
    print('Test2', aA1, aB1, aC1)
    return 100

def Proxy(aFunc: callable, aHash: list[int], *aArgs):
    Args = tuple(map(aArgs.__getitem__, aHash))
    Res = Get(*Args)
    if (not Res):
        Res = aFunc(*aArgs)
        Set(*Args, Res)
    return Res

# q1 = Proxy(Test2, (0, 1), 1, 2, 3)
# print(q1)



async def Main():
    Cnt = 0
    #Cache = TCacheMem('', 10)
    Cache = TCacheFile('Data/cache/temp', 10)
    Cache.Proxy(1,1,2,3)

    for i in range(5):
        Query = {'key1': 1, 'key2': random.randint(0, 5)}
        Data = Cache.Get('common/home', Query)
        if (not Data):
            Cache.Set('common/home', Query, f'Time is {time.time()}')
            Cnt += 1
        asyncio.sleep(0.5)
        print(i, Cnt)


    print('done')


asyncio.run(Main())
print('done')
