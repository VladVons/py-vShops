# Created: 2021.02.28
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import traceback
#
from Inc.Log import TEchoConsole, TEchoFile


class TEchoConsoleEx(TEchoConsole):
    def Write(self, aArgs: dict):
        aE = aArgs.get('aE')
        if (aE):
            traceback.print_exc()
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
