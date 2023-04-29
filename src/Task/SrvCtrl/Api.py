# Created: 2023.03.02
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.DictDef import TDictKey
from Inc.Loader.Lang import TLoaderLangFs
from Inc.Misc.Cache import TCacheMem
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

        Def = GetDictDef(Conf['cache_route'], ['max_age', 'incl_route', 'excl_route'], [5, None, None])
        self.CacheModel = TCacheMem('/', *Def)

        Section = Conf['lang']
        if (Section['type'] == 'fs'):
            Def = GetDictDef(Section, ['default', 'dir'], ['ua', 'MVC/catalog/lang'])
            self.Lang = TLoaderLangFs(*Def)
        else:
            raise ValueError()

    async def GetMethodData(self, aRoute: str, aData: dict) -> dict:
        self.ExecCnt += 1
        Data = self.GetMethod(self.Ctrls, aRoute, aData)
        if ('err' in Data):
            return Data

        Method, Module = (Data['method'], Data['module'])
        return await Method(Module, aData)

    async def Exec(self, aRoute: str, aData: dict) -> dict:
        self.ExecCnt += 1

        Data = self.GetMethod(self.Ctrls, 'system/session', {'method': 'OnExec'})
        await Data['method'](Data['module'], aData)

        Data = self.GetMethod(self.Ctrls, aRoute, aData)
        if ('err' in Data):
            Log.Print(1, 'e', f"TApiCtrl.Exec() {Data['err']}")
            return Data

        Module = Data['module']
        Res = await Data['method'](Module, aData)
        if (not Res):
            Res = {}

        Langs = aData.get('extends', [])
        Langs.append(aData.get('route'))
        for x in Langs:
            await Module.Lang.Add(x)
        Res['lang'] = TDictKey('', Module.Lang.Join())

        Res['modules'] = await Module.LoadModules(aData)
        return Res


ApiCtrl = TApiCtrl()
