# Created: 2022.10.06
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import sys
import time
#
from Inc.ConfJson import TConfJson
from Inc.Util.Mod import DynImport
from IncP.Log import Log


class TPluginApp():
    def __init__(self, aDir: str):
        self.Data = {}
        self.Conf = {}
        self.ConfEx = {}
        self.Path = 'Task.Plugin'
        self.Dir = aDir

    def Init(self, aPlugin: str):
        Dir, ModName = aPlugin.split('.')

        self.Conf = TConfJson()
        Files = [f'{self.Dir}/{Dir}~{ModName}.json', f'{Dir}/{ModName}.json']
        self.Conf.LoadList(Files)

        ConfInclude = self.Conf.get('include', [])
        Files = [f'{self.Dir}/{x}' for x in ConfInclude]
        self.Conf.LoadList(Files, True)

        Conf = self.Conf.get('conf', [])
        self.Conf.LoadList(Conf)
        self.Path = f'{aPlugin}.Plugin'

    async def Load(self, aName: str, aDepth: int) -> dict:
        if (self.Data.get(aName) is None):
            Tab = '-' * (aDepth + 1)
            Log.Print(1, 'i', '%sLoad app %s' % (Tab, aName))

            Depends = self.Conf.GetKey('plugin.' + aName + '.depends', [])
            for Depend in Depends:
                if (not Depend.startswith('-')):
                    if (self.Data.get(Depend) is None):
                        Log.Print(1, 'i', f'{Tab}{aName} depends on {Depend}')
                    await self.Load(Depend, aDepth + 1)

            TClass = DynImport(self.Path + '.' + aName, 'T' + aName)
            if (TClass):
                TimeStart = time.time()
                Class = TClass()
                Class.Parent = self
                Class.Depends = Depends
                Class.Name = aName
                Class.Depth = aDepth
                Class.Conf = TConfJson(self.Conf.JoinKeys(['common', 'plugin.' + aName]))
                ConfEx = self.ConfEx.get(aName, {})
                Class.Conf.update(ConfEx)
                self.Data[aName] = await Class.Run()
                Log.Print(1, 'i', '%sFinish %s. Time: %0.2f' % (Tab, aName, time.time() - TimeStart))
            else:
                Log.Print(1, 'e', '%sErr loading %s' % (Tab, aName))
                sys.exit(1)

    async def Run(self):
        TimeStart = time.time()
        Log.Print(1, 'i', 'Start. TPluginApp.Run()')
        for Plugin in self.Conf.get('plugins', []):
            if (Plugin.get('enable', True)):
                Name = Plugin.get('name')
                Param = Plugin.get('param')
                if (Param):
                    Plugin.ConfEx[Name] = Param
                await self.Load(Name, 0)
        Log.Print(1, 'i', 'Finish. TPluginApp.Run(). Time: %0.2f' % (time.time() - TimeStart))
