# Created: 2024.02.17
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Misc.NovaPoshta import TNovaPoshta
from Inc.Misc.Telegram import TTelegram
from Inc.Util.Mod import DAddModules
from IncP.CtrlBase import TCtrlBase
from . import Api


@DAddModules([Api], '*')
class TMain(TCtrlBase):
    NovaPoshta: TNovaPoshta = None
    Telegram: TTelegram = None

    def _init_(self):
        super()._init_()

        self.DbConf = self.Cache.Get('conf_tenant_0', {})
        self.NovaPoshta = TNovaPoshta(self.DbConf['nova_poshta_token'])
        self.Telegram = TTelegram(self.DbConf['telegram_bot_token'])
