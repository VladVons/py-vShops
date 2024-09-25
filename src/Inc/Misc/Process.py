# Created: 2024.09.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import sys
import psutil


def CheckSelfRunning() -> bool:
    FileMain = getattr(sys.modules['__main__'], '__file__')
    Dir, File = os.path.split(FileMain)

    Pid = os.getpid()
    for proc in psutil.process_iter(['pid', 'cmdline']):
        if proc.info['pid'] != Pid:
            CmdLine = proc.info['cmdline']
            if (CmdLine) and (File in CmdLine) and (Dir == proc.cwd()):
                return True
    return False
