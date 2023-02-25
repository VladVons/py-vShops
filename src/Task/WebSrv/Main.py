# Created: 2021.02.26
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

# https://github.com/aio-libs/aiohttp
# https://docs.aiohttp.org/en/stable/web_advanced.html#aiohttp-web-app-runners


from aiohttp import web
#
from Inc.WebSrv.WebSrv import TWebSrvBase
from IncP.Log import Log
from .Session import Session


class TWebSrv(TWebSrvBase):
    async def _FormCreateUser(self, aRequest: web.Request) -> web.Response: #//
        Name = aRequest.match_info.get('name')

        await Session.Update(aRequest)
        if (not Session.Data.get('user_id')) and (Name not in ['login', 'misc/about']):
            Redirect = f'login?url={Name}'
            raise web.HTTPFound(location = Redirect)

        return await self._FormCreate(aRequest, Name)

    async def _Err_404(self, aRequest: web.Request) -> web.Response:
        #https://docs.aiohttp.org/en/stable/web_advanced.html
        #Routes = web.RouteTableDef()

        Info = f'File not found {aRequest.path}'
        Form  = await self._FormCreate(aRequest, self._SrvConf.def_page, {'info': Info})
        Res = await Form.Render()
        Res.set_status(404, Info)
        return Res

    async def RunApp(self):
        Log.Print(1, 'i', f'WebSrv.RunApp() on port {self.SrvConf.port}')

        ErroMiddleware = {
            404: self._Err_404
        }
        App = self.CreateApp(aErroMiddleware=ErroMiddleware)

        await self.Run(App)
