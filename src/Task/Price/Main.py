# Created: 2022.10.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.PluginApp import TPluginApp
from Task import Options

class TPrice():
    async def Run(self, aParam: dict = None):
        Plugin = TPluginApp(f'Conf/{Options.Conf}')
        Plugin.Init('Task.Price')
        if (isinstance(aParam, dict)):
            for Key, Val in aParam.items():
                Plugin.ConfEx[Key] = Val
        await Plugin.Run()
