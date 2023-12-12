# Created: 2023.02.20
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import time
from aiohttp import web
#
from Inc.Misc.Misc import TJsonEncoder
from Inc.SrvWeb.SrvBase import TSrvBase
from IncP.Log import Log
from .Api import ApiModels


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
            #Path = Data['_path'] #ToDo
            Path = 'catalog'
            Method = Data.get('method')
            Res = await ApiModels[Path].Exec(Name, Data)

        Res['info'] = {
            'module': Name,
            'method': Method,
            'time': round(time.time() - TimeStart, 4),
            'status': Status
        }
        return web.json_response(Res, status=Status, dumps=TJsonEncoder.Dumps)

    @staticmethod
    async def _DbConnect():
        for Key in ApiModels:
            await ApiModels[Key].DbConnect()

    async def _cbOnStartup(self, aApp: web.Application):
        try:
            await self._DbConnect()
            yield
            # wait till working...
        except Exception as E:
            Log.Print(1, 'x', '_cbOnStartup()', aE = E)
        finally:
            Log.Print(1, 'i', '_cbOnStartup(). Close connection')
            await ApiModels.DbClose()

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

        #import asyncio
        #ApiModel.AEvent = asyncio.Event()
        await self._DbConnect()
        #ApiModel.AEvent.set()
