# Created: 2021.02.26
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

# https://github.com/aio-libs/aiohttp
# https://docs.aiohttp.org/en/stable/web_advanced.html#aiohttp-web-app-runners


import os
import re
import jinja2
from aiohttp import web
import aiohttp_jinja2
#
from Inc.SrvWeb.SrvBase import TSrvBase, TSrvConf
from Inc.SrvWeb.Common import FileReader
from Inc.DataClass import DDataClass
from Inc.Misc.Request import TRequestJson, TAuth
from IncP.Log import Log


@DDataClass
class TSrvViewFormConf(TSrvConf):
    ctrl_api: str
    ctrl_user: str
    ctrl_password: str
    dir_3w: str = 'view'
    dir_control: str = 'control'
    dir_tpl: str = 'view'
    dir_tpl_cache: str = 'cache/tpl'
    dir_root: str = 'Task/SrvView'
    tpl_ext: str = '.tpl'
    def_page: str = 'info'
    theme: str = 'theme1'
    deny: str = r'.tpl$|.py$'
    allow: str = r'.html$'


class TSrvViewForm(TSrvBase):
    def __init__(self, aSrvConf: TSrvViewFormConf):
        super().__init__(aSrvConf)
        self._SrvConf = aSrvConf

        Auth = TAuth(self._SrvConf.ctrl_user, self._SrvConf.ctrl_password)
        self.RequestCtrl = TRequestJson(aAuth=Auth)

        self._DirTpl = f'{self._SrvConf.dir_root}/{self._SrvConf.dir_tpl}'
        self._DirPy = f'{self._SrvConf.dir_root}/{self._SrvConf.dir_control}'

    def _GetDefRoutes(self) -> list:
        return [
            web.get('/route/{name:.*}', self._rRoute),
            web.post('/route/{name:.*}', self._rRoute),
            web.get('/{name:.*}', self._rIndex),
            web.post('/{name:.*}', self._rIndex),
        ]

    async def _Err_Page(self, aRequest: web.Request, aText: str, aCode: int) -> web.Response:
        Form  = await self._FormCreate(aRequest, self._SrvConf.def_page, {'info': aText})
        Res = await Form.Render()
        Res.set_status(aCode, aText)
        return Res

    async def _Err_404(self, aRequest: web.Request) -> web.Response:
        return await self._Err_Page(aRequest, f'Path not found {aRequest.path}', 404)

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

    async def _rRoute(self, aRequest: web.Request) -> web.Response:
        Name = aRequest.match_info.get('name')
        Url = f'{self._SrvConf.ctrl_api}/{Name}?{aRequest.query_string}'
        Request = await self.RequestCtrl.Send(Url, {})
        Form = await self._FormCreate(aRequest, Name, Request)
        return await Form.Render()

    async def _rIndex(self, aRequest: web.Request) -> web.Response:
        Name = aRequest.match_info.get('name')
        if (Name):
            File = f'{self._SrvConf.dir_root}/{Name}'
            if (os.path.exists(File)):
                if (re.search(self._SrvConf.deny, Name)):
                    Res = await self._Err_Page(aRequest, f'Access denied {aRequest.path}', 403)
                elif (re.search(self._SrvConf.allow, Name)):
                    with open(File, 'r', encoding='utf8') as F:
                        Data = F.read()
                    Res = web.Response(text=Data)
                else:
                    Headers = {'Content-disposition': 'attachment; filename=%s' % (Name)}
                    # pylint: disable-next=no-value-for-parameter
                    Res = web.Response(body=FileReader(aFile=File), headers=Headers)
            else:
                Res = await self._Err_Page(aRequest, f'File not found {Name}', 404)
        else:
            Form = await self._FormCreate(aRequest, 'common/home')
            Res = await Form.Render()
        return Res

    def CreateApp(self, aRoutes: list = None, aErroMiddleware: dict = None) -> web.Application:
        App = super().CreateApp(aRoutes, aErroMiddleware)
        Loader = jinja2.FileSystemLoader(self._DirTpl)
        aiohttp_jinja2.setup(App, loader=Loader)
        return App

    async def RunApp(self):
        Log.Print(1, 'i', f'SrvViewForm.RunApp() on port {self._SrvConf.port}')

        App = self.CreateApp(aErroMiddleware = {404: self._Err_404})
        await self.Run(App)
