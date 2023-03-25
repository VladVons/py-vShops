# Created: 2023.03.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#
# with TimerLog('FileName'):
#     for _i in range(100_000):
#          MySlowFunc()
#


import os
import sys
import time
import cProfile
import inspect


class _TTimer():
    def __init__(self, aLabel: str = 'timer', aEnable: bool = True):
        self.Label = aLabel
        self.Enable = aEnable
        self.TimeAt: float

    def __enter__(self):
        self._Open()
        self.TimeAt = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if (self.Enable):
            Time = time.time() - self.TimeAt
            self._Close(Time)

    def _Close(self, aTime: float):
        raise NotImplementedError

    def _Format(self, aTime: float):
        Now = time.strftime('%Y-%m-%d %H.%M.%S')
        return f'{Now}, {aTime :.5f}, {self.Label}'

    def _Open(self):
        pass


class TStats(_TTimer):
    # with TStats():
    #     MySlowFunc()
    ProfH: cProfile.Profile

    def _Open(self):
        self.ProfH = cProfile.Profile()
        self.ProfH.enable()
        return self

    def _Close(self, aTime: float):
        self.ProfH.disable()
        # Stats = pstats.Stats(self.ProfH)
        # Stats.sort_stats(pstats.SortKey.TIME)
        # Stats.dump_stats(File)

        File = f'{self.Label}.dat'
        self.ProfH.dump_stats(File)
        print(f'Report saved. To visualize use: snakeviz {File}')


class TTimer(_TTimer):
    def _Close(self, aTime: float):
        Msg = self._Format(aTime)
        print(Msg)


class TTimerLog(_TTimer):
    def __init__(self, aLabel: str = 'timer', aEnable: bool = True, aFile: str = None, aStackLevel: int = 4):
        super().__init__(aLabel, aEnable)
        self.File = aFile or aLabel
        self.StackLevel = aStackLevel

    def _Close(self, aTime: float):
        Msg = self._Format(aTime)
        print(Msg)

        SelfLevel = 2
        Stack = inspect.stack()[SelfLevel:self.StackLevel + SelfLevel]
        AppDir = sys.path[0]
        Chain = [
            f'{os.path.basename(x.filename)}:{x.function}()'
            for x in Stack
            if (AppDir in x.filename)
        ]
        Msg = f'{Msg :45} {", ".join(Chain)}'

        with open(f'{self.File}.log', 'a+', encoding='utf-8') as F:
            F.write(f'{Msg}\n')


def Repeat(aFunc: callable, aArgs: list = None, aCnt: int = 100_000) -> object:
    # Repeat(MySlowFunc, [Arg1, Arg2], 100_000)

    StartAt = time.time()
    for _i in range(aCnt):
        Res = aFunc(*aArgs) if (aArgs) else aFunc()
    Time = time.time() - StartAt
    print(f'{aFunc.__name__}: {Time :.5f}, Loops: {aCnt}, Avg: {Time / aCnt :.5f}')
    return Res
