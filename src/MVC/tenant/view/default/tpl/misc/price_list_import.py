# Created: 2024.02.22
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Obj import DeepGetByList
from IncP.FormBase import TFormBase
from Task.Price.Main import TPrice
from Task.Queue.Main import TCall
from Task import Plugin


class TForm(TFormBase):
    async def _DoRender(self):
        Data = await self.ExecCtrlDef()
        self.out.update(Data)
        if (DeepGetByList(self.out, ['data', 'btn_submit']) is None):
            return

        Alias = DeepGetByList(self.out, ['tenant', 'alias'])
        Param = {
            'conf_name': 'Tenant',
            'conf': [
                {
                    'key': 'plugin.Out_vShopTenant_db.depends',
                    'action': 'set',
                    'val': [f'In_{Alias}']
                }
            ]
        }

        # no wait for result method (ToDo: catch exception inside)
        # await Plugin.Post(self, {
        #     'to': 'TQueue',
        #     'type': 'add',
        #     'call': TCall(TPrice().Run, [Param])
        # })

        # wait for result method
        await TPrice().Run(Param)

        self.out['in_process'] = 'ok'
