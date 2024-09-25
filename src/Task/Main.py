# Created: 2021.02.26
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import time
#
from Inc.IncP.App import TApp
from IncP import GetAppVer
from IncP.Log import Log


class TTask():
    def __init__(self):
        self.Info = GetAppVer()

    async def Run(self):
        if (App.Options.get('info')):
            List = [f'{Key:10} {Val}' for Key, Val in self.Info.items()]
            print('\n'.join(List))
            return

        Log.Print(1, 'i', 'Run() %s' % (self.Info['app_name']))

        TimeStart = time.time()
        try:
            App.LoadPlugins()
            await App.Plugin.Run()
        except KeyboardInterrupt as E:
            Log.Print(1, 'x', 'TTask.Run()', aE = E)
        except Exception as E:
            Log.Print(1, 'x', 'TTask.Run()', aE = E)
            raise E
        finally:
            await App.Plugin.StopAll()
            Log.Print(1, 'i', 'End. Time %0.2f' % (time.time() - TimeStart))

App = TApp()
