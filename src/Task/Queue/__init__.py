# Created: 2022.10.20
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from .Main import TQueue


def Main(_aConf) -> tuple:
    Obj = TQueue()
    return (Obj, Obj.Run())
