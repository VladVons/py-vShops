# Created: 2024.02.17
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Misc.NovaPoshta import TNovaPoshta
from Inc.Util.Mod import DAddModules
from IncP.CtrlBase import TCtrlBase
from . import Api


@DAddModules([Api], '*')
class TMain(TCtrlBase):
    NovaPoshta: TNovaPoshta = None

    def _init_(self):
        super()._init_()
        Conf = self.Cache.Get('conf_tenant_0', {})
        self.NovaPoshta = TNovaPoshta(Conf['nova_poshta_token'])
