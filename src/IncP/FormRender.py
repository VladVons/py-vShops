# Created: 2023.03.22
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.FormBase import TFormBase


class TFormRender(TFormBase):
    async def _DoRender(self):
        Data = await self.ExecCtrlDef()
        self.out.modules = {'inc_right': ['one', 'two', 'three']}