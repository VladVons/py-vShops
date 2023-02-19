# Created: 2022.10.12
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import sys
import argparse
#
from Inc.Conf import TConf
from Inc.PluginTask import TPluginTask
from Inc.Misc.Log import TEchoConsoleEx, TEchoFileEx
from Inc.Misc.Misc import GetEnvWithWarn
from IncP.Log import Log
from IncP import GetInfo


def _InitOptions():
    Usage = f'usage: {AppName} [options] arg'
    Parser = argparse.ArgumentParser(usage = Usage)
    Parser.add_argument('-c', '--Conf',     help='config',            default='Default')
    Parser.add_argument('-i', '--Info',     help='information',       action='store_true')
    Parser.add_argument('-s', '--Service',  help='run as service',    action='store_true')
    return Parser.parse_args()

def _InitLog():
    FileLog = f'/var/log/{AppName}/{AppName}.log'
    if (not os.path.exists(FileLog)) or (not os.access(FileLog, os.W_OK)):
        FileLog = sys.argv[0].removesuffix('.py') + '.log'
    Log.AddEcho(TEchoFileEx(FileLog))
    print(f'Log file {FileLog}')

    Log.AddEcho(TEchoConsoleEx())

AppName = GetInfo()['app_name']
Options = _InitOptions()
_InitLog()

DirConf = f'Conf/{Options.Conf}'
ConfTask = TConf(f'{DirConf}/Task.py')
ConfTask.Load()
ConfTask.Def = {'env_smtp_passw': GetEnvWithWarn('env_smtp_passw', Log)}
Plugin = TPluginTask('Task', DirConf)
