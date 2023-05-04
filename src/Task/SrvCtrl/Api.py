# Created: 2023.03.02
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.DictDef import TDictKey
from Inc.Loader.Lang import TLoaderLangFs
from IncP.ApiBase import TApiBase
from IncP.Plugins import TCtrls
from IncP.LibCtrl import GetDictDef
from IncP.Log import Log


class TApiCtrl(TApiBase):
    def __init__(self):
        super().__init__()

        Conf = self.GetConf()
        self.Ctrls = TCtrls(Conf['dir_route'], self)
        self.InitLoader(Conf['loader'])

        #Def = GetDictDef(Conf['cache_route'], ['max_age', 'incl_route', 'excl_route'], [5, None, None])
        #self.CacheModel = TCacheMem('/', *Def)

        Section = Conf['lang']
        if (Section['type'] == 'fs'):
            Def = GetDictDef(Section, ['default', 'dir'], ['ua', 'MVC/catalog/lang'])
            self.Lang = TLoaderLangFs(*Def)
        else:
            raise ValueError()

    async def _GetConf(self):

        return True

    async def GetMethodData(self, aRoute: str, aData: dict) -> dict:
        self.ExecCnt += 1
        Data = self.GetMethod(self.Ctrls, aRoute, aData)
        if ('err' in Data):
            return Data

        Method, Module = (Data['method'], Data['module'])
        return await Method(Module, aData)

    async def Exec(self, aRoute: str, aData: dict) -> dict:
        self.ExecCnt += 1

        Caller = self.GetMethod(self.Ctrls, 'system/session', {'method': 'OnExec'})
        await Caller['method'](Caller['module'], aData)

        LangRoutes = aData.get('extends', [])
        LangRoutes.append(aData.get('route'))
        for x in LangRoutes:
            await self.Lang.Add(x)
        Lang = TDictKey('', self.Lang.Join())

        Caller = self.GetMethod(self.Ctrls, aRoute, aData)
        if ('err' in Caller):
            Log.Print(1, 'e', f"TApiCtrl.Exec() {Caller['err']}")
            Caller['lang'] = Lang
            return Caller

        Module = Caller['module']
        Res = await Caller['method'](Module, aData)
        if (not Res):
            Res = {}
        Res['lang'] = Lang
        Res['modules'] = await Module.LoadModules(aData)
        return Res


ApiCtrl = TApiCtrl()
