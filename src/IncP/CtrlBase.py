# Created: 2023.03.07
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Misc.Profiler import TTimerLog
from Inc.Loader.Lang import TLoaderLangFs
from Task.SrvCtrl.Api import TApiCtrl
from IncP.LibCtrl import TDbSql, GetDictDef


class TCtrlBase():
    def __init__(self):
        self.ApiCtrl: TApiCtrl
        self.Lang = TLoaderLangFs('ua', 'MVC/catalog/lang') # TODO
        self.ApiModel = None

    def _init_(self):
        self.ApiModel = self.ApiCtrl.Loader['model'].Get

    async def ExecModel(self, aMethod: str, aData: dict) -> dict:
        #Res = await self.ApiCtrl.CacheModel.ProxyA(aMethod, aData, self.ApiModel, [aMethod, aData])
        with TTimerLog('ApiModel', False, aFile = 'Timer'):
            Res = await self.ApiModel(aMethod, aData)
        return Res

    async def ExecSelf(self, aMethod: str, aData: dict) -> dict:
        return await self.ApiCtrl.Exec(aMethod, aData)

    async def LoadModules(self, aData: dict) -> list:
        aTenantId, aLangId = GetDictDef(aData.get('query'), ('tenant', 'lang'), (1, 1))
        Data = await self.ExecModel(
            'system',
            {
                'method': 'Get_Module_RouteLang',
                'param': {'aTenantId': aTenantId, 'aLangId': aLangId, 'aRoute': aData['route']}
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
                Data['lang'] = await self.Lang.Add(Path)
                Data['layout'] = Rec.GetAsDict()
                Res.append(Data)
        return Res
