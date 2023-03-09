# Created: 2022.02.14
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP import GetInfo
from IncP.FormBase import TFormBase


class TForm(TFormBase):
    def _DoInit(self):
        #self.out.title = 'About'
        pass

    async def _DoRender(self):
        self.out.title = 'view/ctrl/misc/about.py'

        Info = GetInfo()
        Info['host'] = self.Request.host
        Info['remote'] = self.Request.remote

        Arr = [f'{Key}: {Val}' for Key, Val in Info.items()]
        self.out.data['info'] = '<br>\n'.join(Arr)
