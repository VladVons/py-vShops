# Created: 2023.02.20
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from aiohttp import web
#
from IncP.Log import Log
from IncP.SrvBaseEx import TSrvBaseEx
from .Api import ApiModels


class TSrvModel(TSrvBaseEx):
    @staticmethod
    async def _DbConnect():
        for Val in ApiModels.values():
            await Val.DbConnect()

    @staticmethod
    async def _DbClose():
        for Val in ApiModels.values():
            await Val.DbClose()

    async def _cbOnStartup(self, aApp: web.Application):
        try:
            await self._DbConnect()
            yield
            # wait here till working...
        except Exception as E:
            Log.Print(1, 'x', '_cbOnStartup()', aE = E)
        finally:
            Log.Print(1, 'i', '_cbOnStartup(). Close connection')
            await self._DbClose()

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

    def GetApi(self) -> object:
        return ApiModels

    async def RunApp(self):
        Log.Print(1, 'i', f'{self.__class__.__name__}.RunApp() on port {self._SrvConf.port}')

        ErroMiddleware = {
            404: self._Err_404,
            'err_all': self._Err_All
        }
        App = self.CreateApp(aErroMiddleware = ErroMiddleware)
        App.cleanup_ctx.append(self._cbOnStartup)

        await self.Run(App)

    async def RunApi(self):
        Log.Print(1, 'i', f'{self.__class__.__name__}.RunApi() only')

        #import asyncio
        #ApiModel.AEvent = asyncio.Event()
        await self._DbConnect()
        #ApiModel.AEvent.set()
