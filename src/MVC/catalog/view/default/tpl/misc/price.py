# Created: 2023.04.19
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.FormBase import TFormBase
from Task import Plugin
from Task.Price.Main import TPrice
from Task.Queue.Main import TCall


class TForm(TFormBase):
    async def _DoRender(self):
        if (self.out.data.btn_ok):
            await Plugin.Post(self, {
                    'to': 'TQueue',
                    'type': 'add',
                    'call': TCall(Func=TPrice().Run)
                })
            pass
