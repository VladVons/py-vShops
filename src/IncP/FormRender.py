# Created: 2023.03.22
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.FormBase import TFormBase


class TFormRender(TFormBase):
    async def _DoRender(self):
        # self.out.data.info = 'INFO'
        # self.out.data.Set('modules.inc_right', ['one', 'two', 'three'])
        # print(self.out.data.modules['inc_right'])
        self.Data['modules'] = {'inc_right': ['one', 'two', 'three']}
        pass
