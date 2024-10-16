import os
import sys
#
from Inc.Misc.FS import DirWalk
from Inc.Misc.Time import SecondsToDHMS
from Inc.Util.ModHelp import GetHelp
from IncP import GetAppVer


async def Api(_self, aPath: str) -> dict:
    Res = []
    for x in DirWalk(aPath, 'Api.py', 'f'):
        ModFile = os.path.splitext(x[0])[0].replace('/', '.')
        Mod = sys.modules.get(ModFile)
        if (not Mod):
            __import__(ModFile)
            Mod = sys.modules.get(ModFile)
        Data = GetHelp(Mod)
        Res.append(Data)
    return Res

async def GetSysInfo(_self) -> dict:
    return GetAppVer()

async def GetDbInfo(self) -> dict:
    Dbl1 = await self.DbMeta.Db.GetDbVersion()
    Dbl2 = await self.DbMeta.Db.GetStat()

    Uptime = SecondsToDHMS(Dbl1.Rec.uptime.seconds)
    Res = {
        'version': Dbl1.Rec.version.split()[:2],
        'uptime': Uptime,
        'name': Dbl1.Rec.db_name,
        'size': round(Dbl1.Rec.size / 1000000, 2),
        'tables': Dbl1.Rec.tables,
        'max_conn': Dbl2.Rec.max_conn,
        'used_conn': Dbl2.Rec.used_conn,
        'backends': Dbl2.Rec.num_backends
    }
    return Res

async def RegSession(self, aIp: str, aOs: str, aBrowser: str, aHost: str, aUAgent: str, aLocation: str) -> dict:
    MaxLen = 128
    Query = f'''
        insert into hist_session
            (ip, os, browser, host, uagent, location)
        values
            ('{aIp}', '{aOs[:16]}', '{aBrowser[:MaxLen]}', '{aHost[:32]}', '{aUAgent[:256]}', '{aLocation}')
        returning (id)
    '''
    return await self.ExecQueryText(Query)

async def Ins_Session(self, aIp: str, aOs: str, aBrowser: str) -> dict:
    Query = f'''
        insert into hist_session
            (ip, os, browser)
        values
            ('{aIp}', '{aOs[:16]}', '{aBrowser[:64]}')
        returning (id)
    '''
    return await self.ExecQueryText(Query)

async def Ins_HistPageView(self, aSessionId: int, aUrl: str) -> dict:
    Query = f'''
        insert into hist_page_view
            (session_id, url)
        values
            ({aSessionId}, '{aUrl}')
    '''
    return await self.ExecQueryText(Query)

async def Get_Module_RouteLang(self, aTenantId: int, aLangId: int, aRoute: str, aTheme: str, aPath: str) -> dict:
    return await self.ExecQuery(
        'fmtGet_Module_RouteLang.sql',
        {'aTenantId': aTenantId, 'aLangId': aLangId, 'aRoute': aRoute, 'aTheme': aTheme, 'aPath': aPath}
    )

async def Get_LayoutLang(self, aTenantId: int, aLangId: int, aRoute: str, aTheme: str, aPath: str) -> dict:
    return await self.ExecQuery(
        'fmtGet_LayoutLang.sql',
        {'aTenantId': aTenantId, 'aLangId': aLangId, 'aRoute': aRoute, 'aTheme': aTheme, 'aPath': aPath}
    )

async def Get_TenantInf(self, aTenantId: int) -> dict:
    return await self.ExecQuery(
        'fmtGet_TenantInf.sql',
        {'aTenantId': aTenantId}
    )

async def Get_TenantConf(self, aTenantId: int, aAttr: str = None) -> dict:
    CondAttr = ''
    if (aAttr):
        CondAttr = f"and attr like '{aAttr}%'"

    return await self.ExecQuery(
        'fmtGet_TenantConf.sql',
        {'aTenantId': aTenantId, 'CondAttr': CondAttr}
    )

async def Get_Auth(self, aMailPhone: str, aPassword: str) -> dict:
    return await self.ExecQuery(
        'fmtGet_Auth.sql',
        {'aMailPhone': aMailPhone, 'aPassword': aPassword}
    )

async def Get_SeoToDict_LangPath(self, aLangId: int, aPath: list[str]) -> dict:
    Arr = [f"(keyword = '{x}' or keyword like '%/{x}')" for x in aPath]
    CondKeyword = ' or\n'.join(Arr)
    return await self.ExecQuery(
        'fmtGet_SeoToDict_LangPath.sql',
        {'aLangId': aLangId, 'CondKeyword': CondKeyword}
    )

async def Get_Seo_ProductsCount(self) -> dict:
    return await self.ExecQuery(
        'fmtGet_Seo_ProductsCount.sql'
    )

async def Get_Langs(self) -> dict:
    return await self.ExecQuery(
        'fmtGet_Langs.sql'
    )

async def Get_ModuleLang(self, aLangId: int, aModuleId: int) -> dict:
    return await self.ExecQuery(
        'fmtGet_ModuleLang.sql',
        {'aLangId': aLangId, 'aModuleId': aModuleId}
    )
