# Created: 2023.03.22
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Misc.Profiler import TTimerLog
from IncP.FormBase import TFormBase


class TFormRender(TFormBase):
    async def _DoRender(self):
        with TTimerLog('ExecCtrlDef', True, aFile='Timer'):
            Data = await self.ExecCtrlDef()
        self.out.update(Data)
