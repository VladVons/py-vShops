# -*- coding: utf-8 -*-
#
# Created: 2022.01.02
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import asyncio
#
from IncP import GetInfo
from Task.Main import TTask


def Run():
    Info = GetInfo()
    PyNeed = (3, 9, 0)
    if (Info['python'] >= PyNeed):
        Task = TTask().Run()
        asyncio.run(Task)
    else:
        print(f'Need python >= {PyNeed}')

if (__name__ == '__main__'):
    Run()
