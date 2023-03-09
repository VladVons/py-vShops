# Created: 2022.04.30
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import sys
import time
import platform
import psutil
#
from Inc.Misc.Time import SecondsToDHMS_Str

TimeStart = time.time()

def GetSysInfo() -> dict:
    UName =  platform.uname()
    CLoad1, CLoad5, CLoad15 = psutil.getloadavg()

    Res = {
        'app_name': os.path.basename(sys.argv[0]).rsplit('.')[0],
        'app_uptime': SecondsToDHMS_Str(time.time() - TimeStart),
        'os': f'{UName.system}, {UName.release}, {UName.processor}',
        'node': platform.node(),
        'host': UName.node,
        'user': os.environ.get('USER'),
        'python': (sys.version_info.major, sys.version_info.minor, sys.version_info.micro),
        'uptime': SecondsToDHMS_Str(time.monotonic()),
        'now': time.strftime('%Y-%m-%d %H:%M:%S'),
        'cpu_use': psutil.cpu_percent(),
        'cpu_load': {'1': round(CLoad1, 2), '5': round(CLoad5, 2), '15': round(CLoad15, 2)},
        'ram_use': psutil.virtual_memory()[2]
    }
    return Res

def DictToText(aData: dict) -> str:
    Arr = [f'{Key}: {Val}' for Key, Val in aData.items()]
    return '\n'.join(Arr)
