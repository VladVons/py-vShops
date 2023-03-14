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
    Dbl1 = await self.DbMeta.Db.GetDbVersion()
    Dbl2 = await self.DbMeta.Db.GetStat()

    Uptime = SecondsToDHMS(Dbl1.Rec.GetField('uptime').seconds)
    Res = {
        'version': Dbl1.Rec.GetField('version').split()[:2],
        'uptime': Uptime,
        'name': Dbl1.Rec.GetField('db_name'),
        'size': round(Dbl1.Rec.GetField('size') / 1000000, 2),
        'tables': Dbl1.Rec.GetField('tables'),
        'max_conn': Dbl2.Rec.GetField('max_conn'),
        'used_conn': Dbl2.Rec.GetField('used_conn'),
        'backends': Dbl2.Rec.GetField('num_backends')
    }
    return Res

async def RegSession(self, aIp: str, aOs: str, aBrowser: str) -> dict:
    Query = f'''
        insert into hist_session (ip, os, browser)
        values ('{aIp}', '{aOs[:16]}', '{aBrowser[:32]}')
        returning (id)
    '''
    return await self.ExecQueryText(Query)

async def AddHistPageView(self, aSessionId: int, aUrl: str) -> dict:
    Query = f'''
        insert into hist_page_view (session_id, url)
        values ({aSessionId}, '{aUrl}')
    '''
    return await self.ExecQueryText(Query)
