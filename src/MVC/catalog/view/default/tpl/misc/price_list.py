# Created: 2022.04.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
#
from Inc.Util.Obj import DeepGetByList
from IncP.FormBase import TFormBase
from Task.Price.Main import TPrice
from Task.Queue.Main import TCall
from Task import Plugin


class TForm(TFormBase):
    async def _DoRender(self):
        Data = await self.ExecCtrlDef()
        self.out.update(Data)

        #if (DeepGetByList(self.out, ['data', 'btn_sitemap']) is not None):
            #ConfDirPrice = self.Parent.Conf.get('dir_price')

        await Plugin.Post(self, {
            'to': 'TQueue',
            'type': 'add',
            'call': TCall(TPrice().Run, [{
                'send_mail': {'to': '123'},
                'conf': 'Tenant'
            }])
        })

        pass