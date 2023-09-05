# Created: 2021.01.30
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


try:
    import asyncio
except ModuleNotFoundError:
    import uasyncio as asyncio

import gc
#
from Inc.Conf import TConf
from Inc.ConfClass import TConfClass
from Inc.Plugin import TPlugin
from IncP.Log import Log


class TPluginTask(TPlugin):
    def GetConf(self, aPath: str) -> list:
        File = '%s/%s~%s' % (self.DirConf, self.Dir, aPath.replace('.', '~'))
        Conf = TConf(File + '.py')
        Conf.Load()
        ConfClass = TConfClass(File + '.class.json', Conf)
        ConfClass.Load()
        return (Conf, ConfClass)

    def _Create(self, aModule, aPath: str) -> tuple:
        gc.collect()
        Log.Print(1, 'i', 'Add task %s' % (aPath))

        if (getattr(aModule, 'skip_main', False) is True):
            return

        Conf, ConfClass = self.GetConf(aPath)
        Arr = aModule.Main(Conf)
        if (Arr):
            Class, AFunc= Arr
            if (Conf) or (ConfClass):
                Class.CC = ConfClass
            return (Class, asyncio.create_task(AFunc))
        return

    async def _Post(self, aTasks, aOwner, aMsg, aFunc) -> dict:
        R = {}
        for Key, (Class, _Task) in aTasks:
            if (Class != aOwner) and (hasattr(Class, aFunc)):
                Func = getattr(Class, aFunc)
                R[Key] = await Func(aOwner, aMsg)
                if (R[Key] == aOwner):
                    break
        return R

    async def Post(self, aOwner, aMsg, aFunc: str = '_DoPost'):
        return await self._Post(self.items(), aOwner, aMsg, aFunc)

    def PostNonAsync(self, aOwner, aMsg, aFunc: str = '_DoPost'):
        return asyncio.create_task(self.Post(aOwner, aMsg, aFunc))

    async def Stop(self, aPath: str) -> bool:
        Obj = self.get(aPath)
        if (Obj):
            await self._Post([(aPath, Obj)], None, None, '_DoStop')
            await asyncio.sleep(0.5)
            Obj[1].cancel()
            del self[aPath]
            return True

    async def StopAll(self):
        for Key in list(self.keys()):
            await self.Stop(Key)

    async def Run(self):
        Tasks = [Task for Class, Task in self.values()]
        await asyncio.gather(*Tasks)
