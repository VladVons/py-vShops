# Created: 2023.03.02
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.ApiBase import TApiBase, TApiConf
from IncP.Plugins import TCtrls


class TApiCtrl(TApiBase):
    def __init__(self):
        super().__init__()
        self.Ctrls: TCtrls = None

    def Init(self, aConf: TApiConf):
        self.Conf = aConf
        self.Ctrls = TCtrls(self.Conf.dir_module, self)
        self.InitMaster()

    async def Exec(self, aModule: str, aQuery: dict) -> dict:
        self.ExecCnt += 1

        if (not self.Ctrls.IsModule(aModule)):
            return {'err': f'Module not found {aModule}', 'code': 404}

        self.Ctrls.LoadMod(aModule)
        ModuleObj = self.Ctrls[aModule]

        Method = aQuery.get('method', 'Main')
        MethodObj = getattr(ModuleObj.Api, Method, None)
        if (MethodObj is None):
            return {'err': f'Method not found {Method}', 'code': 404}

        return await MethodObj(ModuleObj, aQuery)


ApiCtrl = TApiCtrl()
