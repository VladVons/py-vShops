# Created: 2023.10.11
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


def RoundNear(aVal: float, aNear: int) -> int:
    return round(aVal / aNear) * aNear

def SplitNear(aMin: int, aMax: int, aParts: int, aNear: int = 10) -> list[int]:
    Step = (aMax - aMin) // (aParts - 1)
    if (aNear is None):
        aNear = 10 ** (len(str(Step)) - 1)

    return [RoundNear(x, aNear) for x in range(aMin, aMax, Step)]
