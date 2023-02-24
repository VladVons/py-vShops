# Created: 2022.02.14
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP import GetInfo
from .FormBase import TFormBase


class TForm(TFormBase):
    def _DoInit(self):
        self.out.title = 'About'

    async def _Render(self):
        Arr = [f'{Key}: {Val}' for Key, Val in GetInfo().items()]
        self.out.data.info = '<br>\n'.join(Arr)
