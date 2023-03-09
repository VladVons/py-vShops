# Created: 2022.02.14
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Obj import DeepGetByList
from IncP import GetInfo
from IncP.FormBase import TFormBase


class TForm(TFormBase):
    def _DoInit(self):
        #self.out.title = 'About'
        pass

    async def _DoRender(self):
        self.out.title = 'view/ctrl/misc/about.py'
        Data = DeepGetByList(self.out.data_api, ['data', 'data', 'data'])
        DbInfo = [f'{Key}: {Val}' for Key, Val in Data.items()]

        Data = GetInfo()
        Info = [f'{Key}: {Val}' for Key, Val in Data.items()]

        ReqInfo = [
            f'host: {self.Request.host}',
            f'remote: {self.Request.remote}'
        ]

        Res = DbInfo + [''] + ReqInfo + [''] + Info
        self.out.data['info'] = '<br>\n'.join(Res)
