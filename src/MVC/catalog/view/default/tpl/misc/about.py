# Created: 2024.02.09
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#

from IncP.FormBase import TFormBase
from Inc.Util.Obj import GetTree

class TForm(TFormBase):
    async def _DoRender(self):

        Data = await self.ExecCtrlDef()
        self.out.update(Data)

        for x in ['db', 'sys']:
            Arr = [
                f"{Path.lstrip('/')}: {Obj}"
                for Nested, Path, Obj, _Depth in GetTree(Data[x]['data'])
                if (not Nested)
            ]
            self.out[x] = '<br>\n'.join(Arr)

