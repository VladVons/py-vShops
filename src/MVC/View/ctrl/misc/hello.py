# Created: 2022.02.14
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP import LibView
from IncP.LibView import TFormBase, GetTree, GetInfo


class TForm(TFormBase):
    async def _DoRender(self):
        Data = await self.ExecCtrlDef()
        self.out.title = 'view/ctrl/misc/hello.py'
        self.out.data['info'] = '<br>HELLO<br>\n'
