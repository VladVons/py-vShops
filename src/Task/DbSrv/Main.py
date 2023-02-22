# Created: 2023.02.20
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
import asyncio
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

    async def _GetPostData(self, aRequest: web.Request) -> dict:
        Data = await aRequest.text()
        if (Data):
            try:
                Res = json.loads(Data)
            except Exception as E:
                Res = {'err': str(E)}
        else:
            Res = {}
        return Res

    async def _rModel(self, aRequest: web.Request) -> web.Response:
        Name = aRequest.match_info['name']
        Data = await self._GetPostData(aRequest)
        if ('err' not in Data):
            Data = await Api.Exec(Name, Data)
        return web.json_response(Data)

    async def _cbOnStartup(self, aApp: web.Application):
        #aApp['conf'] = self.Conf

        try:
            await Api.DbInit(self._DbConf)
            yield
            # wait till working...
        finally:
            Log.Print(1, 'i', '_cbOnStartup(). Close connection')
            await Api.DbClose()

    def _GetDefRoutes(self) -> list:
        return [
            web.get('/model/{name:.*}', self._rModel),
            web.post('/model/{name:.*}', self._rModel)
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
