# Created: 2023.01.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import asyncio
#
from IncP import GetSysInfo
from IncP.Log import Log
from Task.Main import TTask


def Test():
    pass

def Run():
    Info = GetSysInfo()
    Log.Print(1, 'i', f'os: {Info["os"]}, python: {Info["python"]}, uptime: {Info["uptime"]}')
    PyNeed = (3, 10, 0)
    if (Info['python'] >= PyNeed):
        Task = TTask().Run()
        asyncio.run(Task)
    else:
        print(f'Need python >= {PyNeed}')
    Log.Print(1, 'i', 'Quit')

if (__name__ == '__main__'):
    Test()
    Run()
