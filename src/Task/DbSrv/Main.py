# Created: 2023.02.20
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from aiohttp import web
#
from Inc.Sql.ADb import TDbAuth
from Inc.WebSrv.WebSrv import TSrvBase, TSrvConf
from IncP.Log import Log
from .Api import Api


class TDbSrv(TSrvBase):
    def __init__(self, aSrvConf: TSrvConf, aDbConf: TDbAuth):
        super().__init__(aSrvConf)
        self._DbConf = aDbConf

    async def _rWebApi(self, aRequest: web.Request) -> web.Response:
        Data = {'data': f'ok {aRequest.path}'}
        return web.json_response(Data)

    async def _cbOnStartup(self, aApp: web.Application):
        #aApp['conf'] = self.Conf

        await Api.DbInit(self._DbConf)
        yield
        # wait till working...

        Log.Print(1, 'i', '_cbOnStartup(). Close connection')
        await Api.DbClose()


    def _GetDefRoutes(self) -> list:
        return [
            web.get('/api/{Name:.*}', self._rWebApi),
            web.post('/api/{Name:.*}', self._rWebApi)
        ]

    @staticmethod
    async def _Err_404(aRequest: web.Request) -> web.Response:
        Data = {'err': f'unknown path {aRequest.path}'}
        return web.json_response(Data, status = 404)

    async def RunApp(self):
        Log.Print(1, 'i', f'DbSrv.RunApp() on port {self._SrvConf.port}')

        App = self.CreateApp(aErroMiddleware = {404: self._Err_404})
        App.cleanup_ctx.append(self._cbOnStartup)

        await self.Run(App)
