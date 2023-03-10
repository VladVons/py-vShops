# Created: 2022.03.09
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import sys
#
from IncP.FormBase import TFormBase


class TForm(TFormBase):
    async def _DoRender(self):
        if (self.out.data.btn_ok):
            sys.exit()
