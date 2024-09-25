# Created: 2024.09.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import sys
import psutil


def CheckSelfRunning() -> bool:
    FileMain = getattr(sys.modules['__main__'], '__file__')
    Script = os.path.basename(FileMain)

    Pid = os.getpid()
    for proc in psutil.process_iter(['pid', 'cmdline']):
        if proc.info['pid'] != Pid:
            CmdLine = proc.info['cmdline']
            if CmdLine and (Script in CmdLine):
                return True
    return False
