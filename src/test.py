# Created: 2023.03.19
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import asyncio
import time
import random
import aiohttp
#
from Inc.Misc.Cache import TCacheFile
from Inc.Misc.Profiler import Profiler


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
    Cache = TCacheFile('Data/cache/temp', 10, None, 'common/home')
    for i in range(5):
        Query = {'key1': 1, 'key2': random.randint(0, 5)}
        q1 = hash(frozenset(sorted(Query.items())))
        print(str(q1))

        Data = Cache.Get('common/home', Query)
        if (not Data):
            Cache.Set('common/home', Query, f'Time is {time.time()}')
            Cnt += 1
        asyncio.sleep(0.5)
        print(i, Cnt)


    print('done')


def Test01(aA1, aB1):
    from Inc.DbList import TDbList, TDbRec

    print(aA1, aB1)
    Data = [
            ['User', 'Age', 'Male', 'Price'],
            [
                ['User5', 55, True, 5.67],
                ['User2', 22, True, 2.34],
                ['User6', 66, True, 6.78]
            ]
    ]


    Dbl1 = TDbList(*Data)
    D0 = [10, 20]
    D1 = [11, 21]

    Dbl1.AddFields(['q1', 'q2'], [D0, D1])
    for Idx, Rec in enumerate(Dbl1):
        print(Idx, Rec.Data)

    return 'done'

#asyncio.run(Main())
#print('done')

Res = Profiler(Test01, [1, 2])
print(Res)
