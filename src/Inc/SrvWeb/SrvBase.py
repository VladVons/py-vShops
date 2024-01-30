# Created: 2022.10.19
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#
# https://github.com/aio-libs/aiohttp


import base64
import asyncio
import ssl
from mimetypes import types_map
from aiohttp import web
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp_session import session_middleware
#
from Inc.DataClass import DDataClass
from Inc.Misc.Misc import GetRandStr
from .ErroMiddleware import CreateErroMiddleware
from .Common import FileReader


@DDataClass
class TSrvConf():
    client_max_file_size: int =  10_000_000
    host: str = '0.0.0.0'
    port: int = 8080
    user: str = None
    password: str = None
    allow_ip: list[str] = []
    ssl: dict = None


class TSrvBase():
    def __init__(self, aSrvConf: TSrvConf):
        self._SrvConf = aSrvConf

    def _GetMimeFile(self, aPath: str) -> web.Response:
        Ext = aPath.rsplit('.', maxsplit = 1)[-1]
        Type = types_map.get(f'.{Ext}')
        if (Type):
            # pylint: disable-next=no-value-for-parameter
            Res = web.Response(body=FileReader(aFile=aPath), content_type = Type)
        else:
            Name = aPath.rsplit('/', maxsplit = 1)[-1]
            Headers = {'Content-disposition': f'attachment; filename={Name}'}
            # pylint: disable-next=no-value-for-parameter
            Res = web.Response(body=FileReader(aFile=aPath), headers=Headers)
        return Res

    def _CheckRequestAuth(self, aRequest: web.Request) -> str:
        if  (self._SrvConf.allow_ip) and (aRequest.remote != '127.0.0.1') and (aRequest.remote not in self._SrvConf.allow_ip):
            return False

        if (not self._SrvConf.user):
            return True

        Auth = self._GetRequestAuth(aRequest)
        return (Auth) and (Auth['user'] == self._SrvConf.user) and (Auth['password'] == self._SrvConf.password)

    def _GetRequestAuth(self, aRequest: web.Request) -> dict:
        Auth = aRequest.headers.get('Authorization')
        if (Auth):
            User, Passw = base64.b64decode(Auth.split()[1]).decode().split(':')
            return {'user': User, 'password': Passw}

    def _GetDefRoutes(self) -> list:
        raise NotImplementedError()

    @property
    def SrvConf(self):
        return self._SrvConf

    def CreateApp(self, aRoutes: list = None, aErroMiddleware: dict = None) -> web.Application:
        App = web.Application(client_max_size = self._SrvConf.client_max_file_size)

        if (not aRoutes):
            aRoutes = self._GetDefRoutes()
        App.add_routes(aRoutes)

        Key32 = GetRandStr(32).encode()
        CookieStorage = EncryptedCookieStorage(Key32)
        Middleware = session_middleware(CookieStorage)
        App.middlewares.append(Middleware)

        if (aErroMiddleware):
            Middleware = CreateErroMiddleware(aErroMiddleware)
            App.middlewares.append(Middleware)

        return App

    async def Run(self, aApp: web.Application):
        # await web._run_app(App, host = '0.0.0.0', port = 8080, shutdown_timeout = 60.0, keepalive_timeout = 75.0)
        # https://docs.aiohttp.org/en/stable/web_advanced.html#aiohttp-web-app-runners

        Runner = web.AppRunner(aApp)
        try:
            ### https://stackoverflow.com/questions/51645324/how-to-setup-a-aiohttp-https-server-and-client
            ssl_context = None
            if (self._SrvConf.ssl):
                ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                ssl_context.load_cert_chain(self._SrvConf.ssl['crt'], self._SrvConf.ssl['key'])

            await Runner.setup()
            Site = web.TCPSite(Runner, host = self._SrvConf.host, port = self._SrvConf.port, ssl_context=ssl_context)
            await Site.start()
            while (True):
                await asyncio.sleep(60)
        finally:
            await Runner.cleanup()
