# Created: 2024.08.02
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from base64 import b64decode
from datetime import datetime
from aiohttp import web
#
from Inc.Var.Dict import DeepGetByList
from IncP.FormBase import TFormBase


class TForm(TFormBase):
    async def _DoRender(self):
        Data = await self.ExecCtrlDef()
        self.out.update(Data)
        if (DeepGetByList(self.out, ['data', 'btn_download'])):
            if ('file' in Data):
                Body = b64decode(Data['file'])
                FileName = f'price_1x1_{datetime.now().strftime("%Y%m%d")}.xlsx'
                self.out['response'] = web.Response(
                    body = Body,
                    headers = {
                        'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                        'Content-Disposition': f'attachment; filename="{FileName}"'
                    }
                )
