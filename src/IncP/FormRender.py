# Created: 2023.03.22
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.FormBase import TFormBase


class TFormRender(TFormBase):
    async def _DoRender(self):
        Data = await self.ExecCtrlDef()
        for Key, Val in Data.get('modules', {}).items():
            if ('err' not in Val):
                pass
        self.out.modules = {'inc_right': ['one', 'two', 'three']}
