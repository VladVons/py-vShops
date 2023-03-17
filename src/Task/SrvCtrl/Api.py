# Created: 2023.03.02
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Obj import DeepGetByList
from IncP.ApiBase import TApiBase
from IncP.Log import Log
from IncP.Plugins import TCtrls


class TApiCtrl(TApiBase):
    def __init__(self):
        super().__init__()
        self.Ctrls: TCtrls = None
        self.OnExec = None

    def Init(self, aConf: dict):
        self.Ctrls = TCtrls(aConf['dir_module'], self)
        self.InitLoader(aConf['loader'])

        Data = self.GetMethod('system', {'data': {'method': 'OnExec'}})
        if ('err' in Data):
            Log.Print(1, 'e', Data['err'])
        else:
            self.OnExec = (Data['method'], Data['module'])

    def GetMethod(self, aModule: str, aData: dict) -> dict:
        if (not self.Ctrls.IsModule(aModule)):
            return {'err': f'Module not found {aModule}', 'code': 404}

        self.Ctrls.LoadMod(aModule)
        ModuleObj = self.Ctrls[aModule]

        Method = DeepGetByList(aData, ['data', 'method'], 'Main')
        MethodObj = getattr(ModuleObj.Api, Method, None)
        if (MethodObj is None):
            return {'err': f'Method {Method} not found in module {aModule}', 'code': 404}

        return {'method': MethodObj, 'module': ModuleObj}

    async def Exec(self, aModule: str, aData: dict) -> dict:
        self.ExecCnt += 1

        Data = self.GetMethod(aModule, aData)
        if ('err' in Data):
            return Data

        if (self.OnExec):
            await self.OnExec[0](self.OnExec[1], aData)

        Method, Module = (Data['method'], Data['module'])
        return await Method(Module, aData)


ApiCtrl = TApiCtrl()
