import os
import sys
#
from Inc.Misc.FS import GetFiles
from Inc.Util.ModHelp import GetHelp
from IncP import GetInfo


async def Api(_self, aPath: str) -> dict:
    Res = []
    for xFile in GetFiles(aPath, 'Api.py'):
        ModFile = os.path.splitext(xFile)[0].replace('/', '.')
        Mod = sys.modules.get(ModFile)
        if (not Mod):
            __import__(ModFile)
            Mod = sys.modules.get(ModFile)
        Data = GetHelp(Mod)
        Res.append(Data)
    return Res

async def SysInfo(_self) -> dict:
    return GetInfo()
