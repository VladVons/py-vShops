# Created: 2024.09.13
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import sys
import argparse
#
from Inc.Conf import TConf
from Inc.ConfJson import TConfJson
from Inc.PluginTask import TPluginTask
from Inc.Misc.Log import TEchoConsoleEx, TEchoFileEx
from IncP.Log import Log
from IncP import GetAppVer


def LoadClassConf(aClass: object) -> dict:
    File = f'{DirConf}/{aClass.__module__}.json'
    Res = TConfJson().LoadFile(File)
    return Res

def _LoadAppConf() -> dict:
    Res = {}
    File = f'{DirConf}/App.json'
    if (os.path.exists(File)):
        Res = TConfJson().LoadFile(File)
    return Res

def _InitOptions():
    Usage = f'usage: {AppName} [options] arg'
    Parser = argparse.ArgumentParser(usage = Usage)
    Parser.add_argument('-c', '--conf',     help='config',            default='Default')
    Parser.add_argument('-i', '--info',     help='information',       action='store_true')
    return Parser.parse_args()

def _InitLog():
    FileLog = f'/var/log/{AppName}/{AppName}.log'
    if (not os.path.exists(FileLog)) or (not os.access(FileLog, os.W_OK)):
        FileLog = sys.argv[0].removesuffix('.py') + '.log'

    EchoFileEx = TEchoFileEx(FileLog)
    EchoFileEx.Level = Options.get('log_level', 1)
    Log.AddEcho(EchoFileEx)
    print(f'Log file {FileLog}')

    Log.AddEcho(TEchoConsoleEx())

AppName = GetAppVer()['app_name']
Options = vars(_InitOptions())

DirConf = f'Conf/{Options["conf"]}'
Log.Print(1, 'i', f'Conf dir {DirConf}')

for xKey, xVal in _LoadAppConf().items():
    if (xKey not in Options):
        Options[xKey] = xVal

_InitLog()

ConfTask = TConf(f'{DirConf}/Task.py')
ConfTask.Load()
Plugin = TPluginTask('Task', DirConf)
