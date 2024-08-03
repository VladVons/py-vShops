# Created: 2024.08.02
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from base64 import b64decode
from aiohttp import web
#
from Inc.Util.Obj import DeepGetByList
from IncP.FormBase import TFormBase


class TForm(TFormBase):
    async def _DoRender(self):
        Data = await self.ExecCtrlDef()
        self.out.update(Data)
        if (DeepGetByList(self.out, ['data', 'btn_download'])):
            if ('file' in Data):
                Body = b64decode(Data['file'])
                self.out['response'] = web.Response(
                    body = Body,
                    headers = {
                        'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                        'Content-Disposition': 'attachment; filename="price_1x1.xlsx"'
                    }
                )
