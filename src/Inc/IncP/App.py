# Created: 2024.09.13
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import sys
import time
import asyncio
import argparse
#
from Inc.Conf import TConf
from Inc.ConfJson import TConfJson
from Inc.Log.EchoStack import TEchoConsoleStack, TEchoFileStack
from Inc.Misc.Process import CheckSelfRunning
from Inc.Misc.Info import GetSysInfo
from Inc.PluginTask import TPluginTask
from Inc.Var.Dict import DictUpdate, DictToText, Filter
from IncP.Log import Log
from IncP import GetAppVer


class TApp():
    def __init__(self):
        self.Options = None
        self.DirConf = None
        self.AppName = None
        self.Plugin: TPluginTask = None

        self._Init()

    def _Init(self):
        self.AppName = GetAppVer()['app_name']
        self.Options = vars(self._InitOptions())

        self.DirConf = f'Conf/{self.Options["conf"]}'
        Log.Print(1, 'i', f'Conf dir {self.DirConf}')

        Conf = self._LoadAppConf()
        DictUpdate(self.Options, Conf, False)

        self._InitLog()

    def _LoadAppConf(self) -> dict:
        Res = {}
        File = f'{self.DirConf}/App.json'
        if (os.path.exists(File)):
            Res = TConfJson().LoadFile(File)
        return Res

    def _InitOptions(self):
        Usage = f'usage: {self.AppName} [options] arg'
        Parser = argparse.ArgumentParser(usage = Usage)
        Parser.add_argument('-c', '--conf',     help='config',            default='Default')
        Parser.add_argument('-i', '--info',     help='information',       action='store_true')
        return Parser.parse_args()

    def _InitLog(self):
        FileLog = f'/var/log/{self.AppName}/{self.AppName}.log'
        if (not os.path.exists(FileLog)) or (not os.access(FileLog, os.W_OK)):
            FileLog = sys.argv[0].removesuffix('.py') + '.log'

        EchoFileEx = TEchoFileStack(FileLog)
        EchoFileEx.Level = self.Options.get('log_level', 1)
        EchoFileEx.MsgUniq = self.Options.get('log_uniq', False)

        Log.AddEcho(EchoFileEx)
        print(f'Log file {FileLog}')

        Log.AddEcho(TEchoConsoleStack())

    def LoadClassConf(self, aClass: object) -> dict:
        File = f'{self.DirConf}/{aClass.__module__}.json'
        Res = TConfJson().LoadFile(File)
        return Res

    def LoadPlugins(self):
        ConfTask = TConf(f'{self.DirConf}/Task.py')
        ConfTask.Load()
        Plugins = ConfTask.get('plugins', '')

        self.Plugin = TPluginTask('Task', self.DirConf)
        self.Plugin.LoadList(Plugins)

    async def _RunPlugins(self):
        TimeStart = time.time()
        try:
            self.LoadPlugins()
            await self.Plugin.Run()
        except KeyboardInterrupt as E:
            Log.Print(1, 'x', 'TTask.Run()', aE = E)
        except Exception as E:
            Log.Print(1, 'x', 'TTask.Run()', aE = E)
            raise E
        finally:
            await self.Plugin.StopAll()
            Log.Print(1, 'i', 'End. Time %0.2f' % (time.time() - TimeStart))

    def Run(self):
        Log.Print(1, 'i', '')

        AppVer = DictToText(GetAppVer(), '; ')
        Log.Print(1, 'i', f'{AppVer}')

        SysInfo = GetSysInfo()
        Data = DictToText(Filter(SysInfo, ['os', 'python', 'user', 'uptime']), '; ')
        Log.Print(1, 'i', f'{Data}')

        PyNeed = (3, 10, 0)
        if (SysInfo['python'] >= PyNeed):
            if (self.Options.get('one_instance') and CheckSelfRunning()):
                Log.Print(1, 'i', 'Application is already running')
            elif (self.Options.get('info')):
                print(DictToText(AppVer, '\n'))
            else:
                asyncio.run(self._RunPlugins())
        else:
            print(f'Need python >= {PyNeed}')
        Log.Print(1, 'i', 'Quit')
