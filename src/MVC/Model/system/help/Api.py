import os
import sys
#
from Inc.Misc.FS import GetFiles
from Inc.Misc.Time import SecondsToDHMS
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

async def GetSysInfo(_self) -> dict:
    return GetInfo()

async def GetDbInfo(self) -> dict:
    Dbl = await self.DbMeta.Db.GetDbVersion()
    Uptime = SecondsToDHMS(Dbl.Rec.GetField('uptime').seconds)
    Res = {
        'version': Dbl.Rec.GetField('version').split()[:2],
        'uptime': Uptime,
        'name': Dbl.Rec.GetField('db_name'),
        'size': round(Dbl.Rec.GetField('size') / 1000000, 2),
        'tables': Dbl.Rec.GetField('tables')
    }
    return Res
