# Created: 2023.03.02
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.Plugins import TCtrls
from IncP.ApiBase import TApiBase, TApiConf, TLoaderHttp


class TApiCtrl(TApiBase):
    def __init__(self):
        super().__init__()
        self.Ctrls: TCtrls

    def Init(self, aConf: TApiConf):
        self.Conf = aConf
        self.Conf.dir_module = 'IncP/ctrl'
        self.Ctrls = TCtrls(self.Conf.dir_module)
        self.Master = TLoaderHttp(self.Conf.master_user, self.Conf.master_password, self.Conf.master_api)

    async def Exec(self, aModule: str, aQuery: str) -> dict:
        self.ExecCnt += 1
        if (not self.Ctrls.IsModule(aModule)):
            pass

        Res = {}
        return Res

Api = TApiCtrl()
