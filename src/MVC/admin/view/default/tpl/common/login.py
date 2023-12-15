# Created: 2023.12.15
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from aiohttp import web
#
from Inc.Util.Obj import DeepGetByList
from IncP.FormBase import TFormBase


class TForm(TFormBase):
    async def _DoRender(self):
        Data = await self.ExecCtrlDef()
        self.out.update(Data)
        if (DeepGetByList(self.out, ['data', 'user'])):
            Id = Data.get('id')
            if (Id):
                self.Session['user_id'] = Id
                Redirect = self.Request.query.get('url', '/admin')
                raise web.HTTPFound(location = Redirect)
