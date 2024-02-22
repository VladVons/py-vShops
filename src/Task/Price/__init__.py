# Created: 2022.10.12
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from .Main import TPrice

#Depends = 'Task.Queue'

def Main(_aConf) -> tuple:
    Obj = TPrice()
    return (Obj, Obj.Run())
