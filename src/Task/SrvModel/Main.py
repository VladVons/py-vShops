# Created: 2023.02.20
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import time
from aiohttp import web
#
from Inc.SrvWeb.SrvBase import TSrvBase
from IncP.Log import Log
from .Api import ApiModel


class TSrvModel(TSrvBase):
    async def _rApi(self, aRequest: web.Request) -> web.Response:
        Res = {}

        TimeStart = time.time()
        Name = aRequest.match_info.get('name')
        if (not self._CheckRequestAuth(aRequest)):
            Status = 403
            Res['err'] = 'Authorization failed'
        else:
            Status = 200
            Res = await self._GetRequestJson(aRequest)
            Method = Res.get('method')
            if ('err' not in Res):
                Res = await ApiModel.Exec(Name, Res)

        Res['info'] = {
            'module': Name,
            'method': Method,
            'query': ApiModel.ExecCnt,
            'time': round(time.time() - TimeStart, 4)
        }
        return web.json_response(Res, status=Status)

    async def _cbOnStartup(self, aApp: web.Application):
        try:
            await ApiModel.DbConnect()
            yield
            # wait till working...
        except Exception as E:
            Log.Print(1, 'x', '_cbOnStartup()', aE = E)
        finally:
            Log.Print(1, 'i', '_cbOnStartup(). Close connection')
            await ApiModel.DbClose()

    def _GetDefRoutes(self) -> list:
        return [
            web.get('/api/{name:.*}', self._rApi),
            web.post('/api/{name:.*}', self._rApi),
            web.post('/api', self._rApi)
        ]

    @staticmethod
    async def _Err_404(aRequest: web.Request) -> web.Response:
        Data = {'err': f'unknown path {aRequest.path}'}
        return web.json_response(Data, status = 404)

    async def RunApp(self):
        Log.Print(1, 'i', f'SrvModel.RunApp() on port {self._SrvConf.port}')

        App = self.CreateApp(aErroMiddleware = {404: self._Err_404})
        App.cleanup_ctx.append(self._cbOnStartup)

        await self.Run(App)

    async def RunApi(self):
        Log.Print(1, 'i', 'SrvModel.RunApi() only')
        await ApiModel.DbConnect()
