# Created: 2021.02.28
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import sys
import inspect
import traceback
#
from Inc.Log import TEchoConsole, TEchoFile


class TEchoConsoleEx(TEchoConsole):
    def Write(self, aArgs: dict):
        if (aArgs.get('aE')):
            traceback.print_exc()

        if (aArgs.get('aT') in ['e']):
            Chain = GetStackChain(4, 3)
            aArgs['aM'] += f' <{", ".join(Chain)}>'

        super().Write(aArgs)


class TEchoFileEx(TEchoFile):
    def Write(self, aArgs: dict):
        aE = aArgs.get('aE')
        if (aE):
            Msg = traceback.format_exc()
            aArgs['aM'] += '\n' +  Msg
            super().Write(aArgs)
        else:
            super().Write(aArgs)

def GetStackChain(aStart: int = 1, aLen: int = 2) -> list:
    Stack = inspect.stack()
    Stack = Stack[aStart: aStart + aLen]
    AppDir = sys.path[0]
    Chain = [
        f'{os.path.basename(x.filename)} {x.lineno}:{x.function}()'
        for x in Stack
        if (AppDir in x.filename)
    ]
    return Chain
