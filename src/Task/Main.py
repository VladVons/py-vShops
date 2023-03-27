# Created: 2021.02.26
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import time
#
from IncP import GetInfo
from IncP.Log import Log
from . import Plugin, Options, ConfTask


class TTask():
    def __init__(self):
        self.Info = GetInfo()

    async def Run(self):
        if (Options.info):
            List = [f'{Key:10} {Val}' for Key, Val in self.Info.items()]
            print('\n'.join(List))
            return

        Log.Print(1, 'i', 'Run() %s' % (self.Info['app_name']))

        TimeStart = time.time()
        Plugins = ConfTask.get('plugins', '')
        Plugin.LoadList(Plugins)

        try:
            await Plugin.Run()
        except KeyboardInterrupt as E:
            Log.Print(1, 'x', 'TTask.Run()', aE = E)
        except Exception as E:
            Log.Print(1, 'x', 'TTask.Run()', aE = E)
            raise E
        finally:
            await Plugin.StopAll()
            Log.Print(1, 'i', 'End. Time %0.2f' % (time.time() - TimeStart))
