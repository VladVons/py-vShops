# Created: 2023.02.20
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import time
from aiohttp import web
#
from Inc.SrvWeb.SrvBase import TSrvBase
from IncP.Log import Log
from .Api import ApiCtrl


class TSrvCtrl(TSrvBase):
    def _GetDefRoutes(self) -> list:
        return [
            web.get('/api/{name:.*}', self._rApi),
            web.post('/api/{name:.*}', self._rApi)
        ]

    async def _rApi(self, aRequest: web.Request) -> web.Response:
        Res = {}

        TimeStart = time.time()
        if (not self._CheckRequestAuth(aRequest)):
            Status = 403
            Res['err'] = 'Authorization failed'
        else:
            Status = 200
            Name = aRequest.match_info.get('name')
            Res = await ApiCtrl.Exec(Name, aRequest.query)
        Res['time'] = round(time.time() - TimeStart, 4)
        return web.json_response(Res, status = Status)

    @staticmethod
    async def _Err_404(aRequest: web.Request) -> web.Response:
        Data = {'err': f'unknown path {aRequest.path}'}
        return web.json_response(Data, status = 404)

    async def RunApp(self):
        Log.Print(1, 'i', f'SrvCtrl.RunApp() on port {self._SrvConf.port}')

        App = self.CreateApp(aErroMiddleware = {404: self._Err_404})
        await self.Run(App)

    async def RunApi(self):
        Log.Print(1, 'i', 'SrvCtrl.RunApi() only')