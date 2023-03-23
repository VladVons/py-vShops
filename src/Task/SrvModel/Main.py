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
        TimeStart = time.time()
        Name = aRequest.match_info.get('name')
        if (not self._CheckRequestAuth(aRequest)):
            Status = 403
            Method = ''
            Res = {'err': 'Authorization failed'}
        else:
            Status = 200
            Data = await aRequest.json()
            Method = Data.get('method')
            Res = await ApiModel.Exec(Name, Data)

        Res['info'] = {
            'module': Name,
            'method': Method,
            'count': ApiModel.ExecCnt,
            'time': round(time.time() - TimeStart, 4),
            'status': Status
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

    @staticmethod
    async def _Err_All(_aRequest: web.Request, aStack: dict) -> web.Response:
        return web.json_response({'err': aStack}, status = 500)

    async def RunApp(self):
        Log.Print(1, 'i', f'SrvModel.RunApp() on port {self._SrvConf.port}')

        ErroMiddleware = {
            404: self._Err_404,
            'err_all': self._Err_All
        }
        App = self.CreateApp(aErroMiddleware = ErroMiddleware)
        App.cleanup_ctx.append(self._cbOnStartup)

        await self.Run(App)

    async def RunApi(self):
        Log.Print(1, 'i', 'SrvModel.RunApi() only')
        await ApiModel.DbConnect()
