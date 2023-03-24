# Created: 2023.03.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import time
import cProfile
import pstats


def Profiler(aFunc: callable, aArgs: list = None) -> object:
    with cProfile.Profile() as F:
        Res = aFunc(*aArgs) if (aArgs) else aFunc()
    Stats = pstats.Stats(F)
    Stats.sort_stats(pstats.SortKey.TIME)
    #Stats.print_stats()
    File = f'{aFunc.__name__}.prof'
    Stats.dump_stats(File)
    print(f'To visualize use: snakeviz {File}')
    return Res

def TimeIt(aFunc: callable, aArgs: list = None) -> object:
    StartAt = time.time()
    Res = aFunc(*aArgs) if (aArgs) else aFunc()
    print(f'{aFunc.__name__}: {time.time() - StartAt :.5f}')
    return Res

def Repeat(aFunc: callable, aArgs: list = None, aCnt: int = 100_000) -> object:
    StartAt = time.time()
    for _i in range(aCnt):
        Res = aFunc(*aArgs) if (aArgs) else aFunc()
    Time = time.time() - StartAt
    print(f'{aFunc.__name__}: {Time :.5f}, Loops: {aCnt}, Avg: {Time / aCnt :.5f}')
    return Res
