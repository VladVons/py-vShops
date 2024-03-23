# Created: 2023.03.02
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Loader.Lang import TLoaderLangFs
#from Inc.Misc.Cache import TCacheMem
from Inc.Util.Obj import DeepGetByList, DictUpdate
from IncP.ApiBase import TApiBase
from IncP.Plugins import TCtrls
from IncP.LibCtrl import GetDictDef
from IncP.Log import Log


class TApiCtrl(TApiBase):
    def __init__(self, aName: str, aApiCommon: 'TApiCtrl' = None):
        super().__init__()

        self.Name = aName
        self.ApiCommon = aApiCommon
        Conf = self.GetConf()[aName]
        self.Ctrls = TCtrls(Conf['dir_route'], self)
        self.InitLoader(Conf['loader'])
        self.DefRoute = 'system/def_route'
        #Def = GetDictDef(Conf['cache_route'], ['max_age', 'incl_route', 'excl_route'], [5, None, None])
        #self.Cache = TCacheMem('/', *Def)

        self.Langs = {}
        self.Cached = {}

        Section = Conf['lang']
        if (Section['type'] == 'fs'):
            Def = GetDictDef(Section, ['dir'], ['MVC/catalog/lang'])
            self.Lang = TLoaderLangFs(*Def)
        else:
            raise ValueError()

        Mod = self.Ctrls.LoadMod('system')
        self.BaseCtrl = Mod['system']

    async def _GetConf(self):
        return True

    async def GetMethodData(self, aRoute: str, aData: dict) -> dict:
        self.ExecCnt += 1
        Data = self.GetMethod(self.Ctrls, aRoute, aData)
        if ('err' in Data):
            #Log.Print(1, 'e', f'No route {aRoute}')
            return Data

        Method, Module = (Data['method'], Data['module'])
        return await Method(Module, aData)

    async def ExecForm(self, aRoute: str, aData: dict) -> dict:
        Caller = self.GetMethod(self.Ctrls, 'system/session', {'method': 'OnExec'})
        await Caller['method'](Caller['module'], aData)

        Res = {}
        aData['res'] = Res
        for xRoute in aData.get('extends', []):
            Caller = self.GetMethod(self.Ctrls, xRoute, aData)
            if ('err' not in Caller):
                Data = await Caller['method'](Caller['module'], aData)
                if (Data):
                    Res.update(Data)

        Caller = self.GetMethod(self.Ctrls, aRoute, aData)

        # Language collector
        Routes = aData.get('extends', [])
        Routes.append(aData.get('route'))
        Routes.append('_inc/errors')
        for xRoute in Routes:
            await self.Lang.Add('ua', xRoute, 'tpl')
        Lang = self.Lang.Join()
        Res['lang'] = Lang

        if ('err' in Caller):
            Log.Print(1, 'i', f"TApiCtrl.Exec() {Caller['err']}")
            Res['modules'] = await self.BaseCtrl.LoadModules(aData)
            Data = await self.BaseCtrl.LoadLayout(aData)
            Res.update(Data)
        else:
            Module = Caller['module']
            Res['modules'] = await Module.LoadModules(aData)
            Data = await Module.LoadLayout(aData)
            Res.update(Data)
            Data = await Caller['method'](Module, aData)
            DictUpdate(Res, Data)
            if ('raise_status_code' in aData['query']):
                Res['status_code'] = aData['query']['raise_status_code']
        return Res

    async def ExecApi(self, aRoute: str, aData: dict) -> dict:
        Res = self.GetMethod(self.Ctrls, aRoute, aData)
        if ('err' not in Res):
            Res = await Res['method'](Res['module'], aData)
        return Res

    async def ExecOnce(self, aData: dict):
        Caller = self.GetMethod(self.Ctrls, 'system/lang', {'method': 'GetLangs'})
        self.Langs = await Caller['method'](Caller['module'], aData)

    async def Exec(self, aRoute: str, aData: dict) -> dict:
        if (self.ExecCnt == 0):
            await self.ExecOnce(aData)
        self.ExecCnt += 1

        if (aData.get('type') == 'api'):
            Res = await self.ExecApi(aRoute, aData)
        else:
            Res = await self.ExecForm(aRoute, aData)
        return Res


class TApiCtrlAuth(TApiCtrl):
    async def Exec(self, aRoute: str, aData: dict) -> dict:
        if (DeepGetByList(aData, ['session', 'auth_path']) == self.Name) or \
            (aRoute in ['common/login', 'system/session']):
            Res = await super().Exec(aRoute, aData)
        else:
            Msg = f'no session auth in {type(self).__name__}'
            Log.Print(1, 'i', Msg)
            Res = {'err': Msg}
        return Res

ApiCommon = TApiCtrl('_common')
ApiCtrls = {
    'catalog': TApiCtrl('catalog', ApiCommon),
    'tenant': TApiCtrlAuth('tenant', ApiCommon)
}
