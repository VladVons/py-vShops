# Created: 2023.01.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import asyncio
#
from Inc.Var.Dict import DictToText, Filter
from Inc.Misc.Info import GetSysInfo
from Inc.Misc.Process import CheckSelfRunning
from IncP import GetAppVer
from IncP.Log import Log
from Task.Main import TTask, App


def Run():
    Log.Print(1, 'i', '')

    AppVer = DictToText(GetAppVer(), '; ')
    Log.Print(1, 'i', f'{AppVer}')

    SysInfo = GetSysInfo()
    Data = DictToText(Filter(SysInfo, ['os', 'python', 'user', 'uptime']), '; ')
    Log.Print(1, 'i', f'{Data}')

    PyNeed = (3, 10, 0)
    if (SysInfo['python'] >= PyNeed):
        if (App.Options.get('one_instance') and CheckSelfRunning()):
            Log.Print(1, 'i', 'Application is already running')
        else:
            Task = TTask().Run()
            asyncio.run(Task)
    else:
        print(f'Need python >= {PyNeed}')
    Log.Print(1, 'i', 'Quit')

if (__name__ == '__main__'):
    Run()
