# Created: 2022.10.19
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import asyncio
from aiohttp import web
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import aiohttp_jinja2
import aiohttp_session
import jinja2
#
from Inc.Conf import TConf
from Inc.DataClass import DDataClass
from .Common import FileReader


@DDataClass
class TSrvConf():
    client_max_file_size: int = 1024**2
    host: str = '0.0.0.0'
    port: int = 8080

@DDataClass
class TSrvWebConf(TSrvConf):
    dir_3w: str = 'view'
    dir_download: str = 'download'
    dir_control: str = 'control'
    dir_tpl: str = 'view'
    dir_tpl_cache: str = 'cache/tpl'
    dir_root: str = 'Task/WebSrv'
    tpl_ext: str = '.tpl'
    def_page: str = 'info'
    theme: str = 'theme1'

def CreateErroMiddleware(aOverrides):
    @web.middleware
    async def ErroMiddleware(request: web.Request, handler):
        try:
            return await handler(request)
        except web.HTTPException as E:
            Override = aOverrides.get(E.status)
            if (Override):
                return await Override(request)
            raise E
        #except Exception as E:
        #    pass
    return ErroMiddleware


class TSrvBase():
    def __init__(self, aSrvConf: TSrvConf):
        self._SrvConf = aSrvConf

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

        if (aErroMiddleware):
            Middleware = CreateErroMiddleware(aErroMiddleware)
            App.middlewares.append(Middleware)

        aiohttp_session.setup(App, EncryptedCookieStorage(b'my 32 bytes key. qwertyuiopasdfg'))
        return App

    async def Run(self, aApp: web.Application):
        ## pylint: disable-next=protected-access
        ## await web._run_app(App, host = '0.0.0.0', port = 8080, shutdown_timeout = 60.0,  keepalive_timeout = 75.0)

        Runner = web.AppRunner(aApp)
        try:
            await Runner.setup()
            Site = web.TCPSite(Runner, host = self._SrvConf.host, port = self._SrvConf.port)
            await Site.start()
            while (True):
                await asyncio.sleep(60)
        finally:
            await Runner.cleanup()


class TSrvBaseWeb(TSrvBase):
    def __init__(self, aSrvConf: TSrvWebConf, aConf: TConf):
        super().__init__(aSrvConf)
        self._SrvConf = aSrvConf
        self._Conf = aConf

        self._DirTpl = f'{self._SrvConf.dir_root}/{self._SrvConf.dir_tpl}'
        self._DirPy = f'{self._SrvConf.dir_root}/{self._SrvConf.dir_control}'

    @staticmethod
    def _LocateFile(aList: list[str], aDir: str = '') -> str:
        for x in aList:
            Path = aDir + x
            if (os.path.exists(Path)):
                return x

    async def _FormCreate(self, aRequest: web.Request, aName: str, aData: dict = None) -> web.Response:
        FileTpl = self._LocateFile(
            [
                f'{self._SrvConf.theme}/tpl/{aName}{self._SrvConf.tpl_ext}',
                f'default/tpl/{aName}{self._SrvConf.tpl_ext}',
            ],
            self._DirTpl + '/')

        if (FileTpl):
            FilePy = f'{self._DirPy}/{aName}'
        else:
            FilePy = f'{self._DirPy}/{self._SrvConf.def_page}'
            FileTpl = f'default/tpl/{self._SrvConf.def_page}'

        Locate = [
            (FilePy, 'TForm'),
            (f'{self._DirPy}/FormBase', 'TFormBase')
        ]

        TClass = None
        for Module, Class in Locate:
            try:
                if (os.path.isfile(Module + '.py')):
                    Mod = __import__(Module.replace('/', '.'), None, None, [Class])
                    TClass = getattr(Mod, Class)
                    break
            except ModuleNotFoundError as _E:
                pass
        Res = TClass(aRequest, FileTpl, aData)
        Res.Parent = self
        return Res

    async def _FormCreateUser(self, aRequest: web.Request) -> web.Response:
        raise NotImplementedError()

    async def _rDownload(self, aRequest: web.Request) -> web.Response:
        Name = aRequest.match_info['name']
        File = '%s/%s/%s' % (self._SrvConf.dir_root, self._SrvConf.dir_download, Name)
        if (not os.path.exists(File)):
            return web.Response(body='File %s does not exist' % (Name), status=404)

        Headers = {'Content-disposition': 'attachment; filename=%s' % (Name)}
        # pylint: disable-next=no-value-for-parameter
        return web.Response(body=FileReader(aFile=File), headers=Headers)

    async def _rForm(self, aRequest: web.Request) -> web.Response:
        Form = await self._FormCreateUser(aRequest)
        return await Form.Render()

    async def _rIndex(self, aRequest: web.Request) -> web.Response:
        Name = aRequest.match_info['name']
        Form = await self._FormCreate(aRequest, 'index')
        return await Form.Render()

    def _GetDefRoutes(self) -> list:
        return [
            web.get('/form/{name:.*}', self._rForm),
            web.post('/form/{name:.*}', self._rForm),
            web.get('/{name:.*}', self._rIndex),
        ]

    def CreateApp(self, aRoutes: list = None, aErroMiddleware: dict = None) -> web.Application:
        App = super().CreateApp(aRoutes, aErroMiddleware)

        Path = f'{self._SrvConf.dir_root}/{self._SrvConf.dir_3w}'
        #App.router.add_static('/', Path, show_index=True, follow_symlinks=True, expect_handler=self.OnExpect)

        # https://python.hotexamples.com/examples/jinja2/Environment/compile_templates/python-environment-compile_templates-method-examples.html
        #DirCache = f'{self._SrvConf.dir_root}/{self._SrvConf.dir_tpl_cache}'
        #Env = jinja2.Environment(loader = jinja2.FileSystemLoader(self._DirTpl))
        #Env.compile_templates(DirCache, ['tpl'])

        Loader = jinja2.ChoiceLoader([
        #    jinja2.ModuleLoader(DirCache),
            jinja2.FileSystemLoader(self._DirTpl)
        ])

        aiohttp_jinja2.setup(App, loader=Loader)
        return App
