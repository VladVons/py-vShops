# Created: 2023.03.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import cProfile
import pstats


def Profiler(aFunc, aArgs):
    with cProfile.Profile() as F:
        Res = aFunc(*aArgs)
        Stats = pstats.Stats(F)
        Stats.sort_stats(pstats.SortKey.TIME)
        #Stats.print_stats()
        Stats.dump_stats(f'{aFunc.__name__}.prof')
        return Res
