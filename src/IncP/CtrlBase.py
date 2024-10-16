# Created: 2023.03.07
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Misc.Cache import TCacheMem
from Inc.Misc.Profiler import TTimerLog
from Inc.Loader.Lang import TLoaderLang
from Task.SrvCtrl.Api import TApiCtrl
import IncP.LibCtrl as Lib


class TCtrlBase():
    def __init__(self, aApiCtrl: TApiCtrl):
        self.ApiCtrl = aApiCtrl
        self.ApiModel = None
        self.ApiImg = None
        self.Cache = TCacheMem(aMaxAge = 30)

    def _init_(self):
        self.ApiModel = self.ApiCtrl.Loader['model'].Get
        self.ApiImg = self.ApiCtrl.Loader['img'].Get

    @property
    def Common(self) -> TApiCtrl:
        return self.ApiCtrl.ApiCommon.Ctrls.ApiCtrl

    @property
    def Lang(self) -> TLoaderLang:
        return self.ApiCtrl.Lang

    @property
    def Name(self) -> str:
        return self.ApiCtrl.Name

    def GetLangId(self, aAlias: str) -> int:
        return self.ApiCtrl.Langs.get(aAlias, 1)

    async def ExecImg(self, aMethod: str, aData: dict) -> dict:
        return await self.ApiImg(aMethod, aData)

    async def ExecModel(self, aMethod: str, aData: dict) -> dict:
        #Res = await self.ApiCtrl.CacheModel.ProxyA(aMethod, aData, self.ApiModel, [aMethod, aData])
        with TTimerLog('ApiModel', False, aFile = 'Timer'):
            Res = await self.ApiModel(aMethod, aData)
        return Res

    async def ExecModelImport(self, aMethod: str, aData: dict) -> dict:
        Data = await self.ApiModel(aMethod, aData)
        DblData = Data.get('data')
        if (DblData):
            return Lib.TDbSql().Import(DblData)

    async def ExecModelExport(self, aMethod: str, aData: dict) -> dict:
        Dbl = await self.ExecModelImport(aMethod, aData)
        if (Dbl):
            return Dbl.Export()

    async def ExecSelf(self, aRoute: str, aData: dict) -> dict:
        return await self.ApiCtrl.GetMethodData(aRoute, aData)

    async def GetConf(self, _aData: dict) -> dict:
        Res = await self.ExecModel(
            'system',
            {
                'method': 'Get_TenantConf',
                'param': {'aTenantId': 0}
            }
        )
        DblConf = Lib.TDbSql().Import(Res['data'])
        return DblConf.ExportPair('attr', 'val')


    async def LoadLayout(self, aData: dict) -> dict:
        aTenantId, aLang = Lib.GetDictDef(
            aData.get('query'),
            ('tenant', 'lang'),
            (1, 'ua'))

        DblData = await self.ExecModel(
            'system',
            {
                'method': 'Get_LayoutLang',
                'param': {'aTenantId': aTenantId, 'aLangId': self.GetLangId(aLang), 'aRoute': aData['route'], 'aTheme': 't2', 'aPath': aData['_path']}
            }
        )
        Dbl = Lib.TDbSql().Import(DblData.get('data'))
        return Dbl.Rec.GetAsDict()


    async def LoadModules(self, aData: dict) -> list:
        aTenantId, aLang = Lib.GetDictDef(
            aData.get('query'),
            ('tenant', 'lang'),
            (1, 'ua'))

        Path = aData['_path']
        DblData = await self.ExecModel(
            'system',
            {
                'method': 'Get_Module_RouteLang',
                'param': {'aTenantId': aTenantId, 'aLangId': self.GetLangId(aLang), 'aRoute': aData['route'], 'aTheme': 't2', 'aPath': Path}
            }
        )

        Res = []
        Modules = DblData.get('data')
        if (Modules):
            Dbl = Lib.TDbSql().Import(Modules)
            for Rec in Dbl:
                Module = Rec.code
                Path = f'module/{Module}'
                aData['rec'] = Rec.GetAsDict()
                Data = await self.ExecSelf(Path, aData)
                if (Data is None):
                    Data = {}
                Data['lang'] = await self.Lang.Add('ua', Path)
                Data['layout'] = Rec.GetAsDict()
                Res.append(Data)
        return Res
