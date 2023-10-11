# Created: 2023.10.11
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


def RoundNear(aVal: float, aNear: int) -> int:
    return round(aVal / aNear) * aNear
