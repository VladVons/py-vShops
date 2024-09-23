# Created: 2022.10.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Dict import DeepSet
from Inc.PluginApp import TPluginApp
from Task import Options

class TPrice():
    async def Run(self, aParam: dict = None):
        Dir = f'Conf/{Options.conf}/{aParam["conf_name"]}'
        Plugin = TPluginApp(Dir)
        Plugin.Init('Task.Price')
        for x in aParam.get('conf'):
            if (x['action'] == 'set'):
                DeepSet(Plugin.Conf, x['key'], x['val'])

        if (isinstance(aParam, dict)):
            for Key, Val in aParam.items():
                Plugin.ConfEx[Key] = Val
        await Plugin.Run()
