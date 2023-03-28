# Created: 2023.03.22
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.DbList import TDbList
#from Inc.DictDef import TDictDef
from Inc.Misc.Profiler import TTimerLog
from IncP.FormBase import TFormBase


class TFormRender(TFormBase):
    async def _DoRender(self):
        with TTimerLog('ExecCtrlDef', True, aFile='Timer'):
            Data = await self.ExecCtrlDef()

        # Out = {}
        # for Key, Val in Data.get('modules', {}).items():
        #     if ('err' not in Val):
        #         Out[Key] = {
        #             'data': TDbList().Import(Val.get('data')),
        #             'lang': Val.get('lang')
        #         }
        self.out.ctrl = Data
        pass
