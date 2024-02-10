# Created: 2024.02.09
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.FormBase import TFormBase
from Inc.Util.Obj import GetTree

class TForm(TFormBase):
    async def _DoRender(self):

        Data = await self.ExecCtrlDef()
        Arr = [
            f"{Path.lstrip('/')}: {Obj}"
            for _Nested, Path, Obj, _Depth in GetTree(Data['data'])
        ]
        Info = {'info': '<br>\n'.join(Arr)}
        self.out.update(Data | Info)
