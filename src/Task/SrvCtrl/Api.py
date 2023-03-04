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
        self.Conf.dir_module = 'IncP/ctrl'
        self.Ctrls = TCtrls(self.Conf.dir_module)
        self.InitMaster()

    async def Exec(self, aModule: str, aQuery: str) -> dict:
        self.ExecCnt += 1
        if (not self.Ctrls.IsModule(aModule)):
            return {'err': f'Module not found {aModule}', 'code': 404}

        self.Ctrls.LoadMod(aModule)
        ModuleObj = self.Ctrls[aModule]
        return await ModuleObj.Main(self, aQuery)

ApiCtrl = TApiCtrl()
