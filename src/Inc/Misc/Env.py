# Created: 2022.04.11
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os


def GetEnvWithWarn(aName: str, aLog) -> object:
    Res = os.getenv(aName)
    if (Res is None):
        aLog.Print(1, 'e', f'Warn! environment variable {aName} is empty')
    return Res
