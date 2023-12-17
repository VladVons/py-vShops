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
            AuthId = Data.get('auth_id')
            if (AuthId):
                AuthPath = Data.get('auth_path')
                self.Session['auth_id'] = AuthId
                self.Session['auth_path'] = AuthPath
                Redirect = self.Request.query.get('url', f'/{AuthPath}')
                raise web.HTTPFound(location = Redirect)
