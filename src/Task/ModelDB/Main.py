# Created: 2022.03.16
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import asyncio
from aiohttp import web
#
from Inc.UtilP.Misc import TJsonEncoder
from IncP.Log import Log
from IncP.ApiWeb import TWebSockSrv
from .Api import Api


class TScraperSrv():
    def __init__(self, aConf: dict):
        self.Conf = aConf

        self.WebSockSrv = TWebSockSrv()
        #self.WebSockSrv.Api = Api

    async def cbOnStartup(self, aApp: web.Application):
        aApp['Conf'] = self.Conf

        await Api.DbInit(self.Conf.DbAuth)
        yield
        # wait till working...

        Log.Print(1, 'i', 'cbInit(). Close connection')
        await Api.DbClose()

    async def _rWebApi(self, aRequest: web.Request) -> web.Response:
        #await self.WebSockServer.SendAll({'hello': 111}, '/ws/test')
        if (await Api.AuthRequest(aRequest, self.Conf.Auth)):
            #Conf = aRequest.app.get('Conf')
            Name = aRequest.match_info.get('Name')
            Post = await aRequest.json()

            # ToDo. Test for safety
            #Res = await asyncio.shield(Api.Call(Name, Post))

            Res = await Api.Call(Name, Post)
            return web.json_response(Res, dumps=TJsonEncoder.Dumps)

        Res = {'Type': 'Err', 'Data': 'Authorization failed'}
        return web.json_response(Res, status=403)

    async def _rWebSock(self, aRequest: web.Request) -> web.WebSocketResponse:
        if (await Api.AuthRequest(aRequest, self.Conf.Get('Auth'))):
            return await self.WebSockSrv.Handle(aRequest)

        WS = web.WebSocketResponse()
        await WS.prepare(aRequest)
        await WS.send_json({'Type': 'Err', 'Data': 'Authorization failed'})

    async def Run(self, aSleep: int = 10):
        App = web.Application()
        #App['SomeKey'] = 'Hello'

        #App.on_startup.append(self.cbOnStartup)
        App.cleanup_ctx.append(self.cbOnStartup)

        App.add_routes([
            web.get('/web/{Name:.*}', self._rWebApi),
            web.post('/web/{Name:.*}', self._rWebApi),
            web.get('/ws/{Name:.*}', self._rWebSock)
        ])

        Port = self.Conf.get('Port', 8081)
        while (True):
            try:
                Log.Print(1, 'i', 'ScraperSrv on port %s' % (Port))
                # pylint: disable-next=protected-access
                await web._run_app(App, host = '0.0.0.0', port = Port, shutdown_timeout = 60.0,  keepalive_timeout = 75.0)
            except Exception as E:
                await asyncio.sleep(2)
                Log.Print(1, 'x', 'Run()', aE = E)
            await asyncio.sleep(aSleep)
