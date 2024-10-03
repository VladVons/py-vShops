# Created: 2022.10.06
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import time
#
from Inc.ConfJson import TConfJson
from Inc.Util.Mod import DynImport
from Inc.Var.Dict import DeepGetByList
from Inc.Var.DictEx import DictUpdateDeep
from Inc.Var.Obj import Iif
from IncP.Log import Log


class TPluginApp():
    def __init__(self, aDir: str):
        self.Dir = aDir

        self.Data = {}
        self.Conf = {}
        self.ConfEx = {}
        self.Path = None

    def Init(self, aPlugin: str, aPathRoot: str = None):
        self.Path = Iif (aPathRoot, aPathRoot, f'{aPlugin}.Plugin')

        Dir, ModName = aPlugin.rsplit('.', maxsplit=1)

        self.Conf = TConfJson()
        Files = [f'{self.Dir}/{Dir}~{ModName}.json', f'{Dir}/{ModName}.json']
        self.Conf.LoadList(Files)
        if (self.Conf):
            Conf = self.Conf.get('include', [])
            if (Conf):
                Files = [f'{self.Dir}/{x}' for x in Conf if (not x.startswith('-'))]
                self.Conf.LoadList(Files, True, True)

            Conf = self.Conf.get('conf', [])
            if (Conf):
                self.Conf.LoadList(Conf)
        else:
            Log.Print(3, 'i', f'No conf found in {Files}')

    async def Load(self, aName: str, aDepth: int):
        if (self.Data.get(aName) is None):
            Tab = '-' * (aDepth + 1)
            Log.Print(1, 'i', f'{Tab}Load app {aName}')

            Joins = self.Conf.GetKey(f'plugin.{aName}.joins')
            if (Joins):
                self.ConfEx = DictUpdateDeep(self.ConfEx, Joins)

            Depends = self.Conf.GetKey(f'plugin.{aName}.depends', [])
            for Depend in Depends:
                if (not Depend.startswith('-')):
                    if (self.Data.get(Depend) is None):
                        Log.Print(1, 'i', f'{Tab}{aName} depends on {Depend}')
                    await self.Load(Depend, aDepth + 1)

            TimeStart = time.time()
            Plugin = DeepGetByList(self.Conf, ['plugin', aName])
            assert(Plugin is not None), f'plugin key not found {aName}'
            ClassName = Plugin.get('class', aName)
            TClass, Err = DynImport(self.Path + '.' + ClassName, 'T' + ClassName.replace('.', '_'))
            assert(TClass), f'Err loading {aName}. {Err}'

            Conf = TConfJson(self.Conf.JoinKeys(['common', 'plugin.' + aName]))
            ConfEx = self.ConfEx.get(aName)
            if (ConfEx):
                #Conf.update(ConfEx)
                Conf.Init(DictUpdateDeep(Conf, ConfEx))
            Class = TClass(self, Depends, ClassName, aName, Conf, aDepth)
            Res = await Class.Run()
            if (isinstance(Res, dict)) and (Res.get('cached')) and (DeepGetByList(self.Conf, ['common', 'save_cache'])):
                Log.Print(1, 'i', f'{Tab}{aName} cached. Skip')
            else:
                self.Data[aName] = Res
            Duration = time.time() - TimeStart
            Log.Print(1, 'i', f'{Tab}Finish {aName}. Time: {Duration:.2f}')

    async def Run(self):
        TimeStart = time.time()
        Log.Print(1, 'i', 'Start. TPluginApp.Run()')
        for Plugin in self.Conf.get('plugins', []):
            if (not Plugin.startswith('-')):
                await self.Load(Plugin, 0)
        Log.Print(1, 'i', 'Finish. TPluginApp.Run(). Time: %0.2f' % (time.time() - TimeStart))
