# Created: 2023.03.07
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Misc.Cache import TCacheMem
from Inc.Misc.Profiler import TTimerLog
from Inc.Loader.Lang import TLoaderLang
from Task.SrvCtrl.Api import TApiCtrl
from IncP.LibCtrl import TDbSql, GetDictDef


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
    def Lang(self) -> TLoaderLang:
        return self.ApiCtrl.Lang

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
            return TDbSql().Import(DblData)

    async def ExecModelExport(self, aMethod: str, aData: dict) -> dict:
        Dbl = await self.ExecModelImport(aMethod, aData)
        return Dbl.Export()

    async def ExecSelf(self, aRoute: str, aData: dict) -> dict:
        return await self.ApiCtrl.GetMethodData(aRoute, aData)

    async def GetConf(self, _aData: dict) -> dict:
        Res = await self.ExecModel(
            'system',
            {
                'method': 'Get_ConfTenant',
                'param': {'aTenantId': 0}
            }
        )
        return Res.get('data')

    async def LoadModules(self, aData: dict) -> list:
        aTenantId, aLang = GetDictDef(
            aData.get('query'),
            ('tenant', 'lang'),
            (1, 'ua'))
        Data = await self.ExecModel(
            'system',
            {
                'method': 'Get_Module_RouteLang',
                'param': {'aTenantId': aTenantId, 'aLang': aLang, 'aRoute': aData['route']}
            }
        )

        Res = []
        Modules = Data.get('data')
        if (Modules):
            Dbl = TDbSql().Import(Modules)
            for Rec in Dbl:
                Module = Rec.code
                Path = f'module/{Module}'
                aData['rec'] = Rec.GetAsDict()
                Data = await self.ExecSelf(Path, aData)
                Data['lang'] = await self.Lang.Add('ua', Path)
                Data['layout'] = Rec.GetAsDict()
                Res.append(Data)
        return Res
