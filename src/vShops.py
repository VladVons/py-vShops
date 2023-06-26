# Created: 2023.01.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import asyncio
#
from IncP import GetSysInfo
from Task.Main import TTask


def Run():
    Info = GetSysInfo()
    PyNeed = (3, 9, 0)
    if (Info['python'] >= PyNeed):
        Task = TTask().Run()
        asyncio.run(Task)
    else:
        print(f'Need python >= {PyNeed}')

if (__name__ == '__main__'):
    #Run()
    File = '/long/path/file.jpg'.rsplit('/', maxsplit=1)[-1].split('.', maxsplit=1)[0]
    print(f'{File[0]}{File[-1]}')
    pass

