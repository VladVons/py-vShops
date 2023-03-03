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
from Inc.DataClass import DDataClass
from Inc.SrvWeb import TSrvBase, TSrvConf, FileReader
from IncP.Log import Log
from .Api import Api


@DDataClass
class TSrvViewConf(TSrvConf):
    # dir_3w: str = 'view'
    # dir_tpl: str = 'view'
    # dir_tpl_cache: str = 'cache/tpl'
    # dir_root: str = 'Task/SrvView'
    # tpl_ext: str = '.tpl'
    # def_page: str = 'info'
    # theme: str = 'theme1'
    deny: str = r'.tpl$|.py$'
    allow: str = r'.html$'



class TSrvView(TSrvBase):
    def __init__(self, aSrvConf: TSrvViewConf):
        super().__init__(aSrvConf)
        self._SrvConf = aSrvConf

        self._DirTpl = f'{self._SrvConf.dir_root}/{self._SrvConf.dir_tpl}'
        self._DirPy = f'{self._SrvConf.dir_root}/{self._SrvConf.dir_control}'

    def _GetDefRoutes(self) -> list:
        return [
            web.get('/api/{name:.*}', self._rApi),
            web.post('/api/{name:.*}', self._rApi),
            web.get('/{name:.*}', self._rIndex),
            web.post('/{name:.*}', self._rIndex),
        ]

    async def _Err_Page(self, aRequest: web.Request, aText: str, aCode: int) -> web.Response:
        Form  = await Api.FormCreate(aRequest, self._SrvConf.def_page, {'info': aText})
        Res = await Form.Render()
        Res.set_status(aCode, aText)
        return Res

    async def _Err_404(self, aRequest: web.Request) -> web.Response:
        return await self._Err_Page(aRequest, f'Path not found {aRequest.path}', 404)

    async def _rApi(self, aRequest: web.Request) -> web.Response:
        Name = aRequest.match_info.get('name')
        # Url = f'{self._SrvConf.ctrl_api}/{Name}?{aRequest.query_string}'
        # Request = await self.RequestCtrl.Send(Url, {})
        Form = await Api.FormCreate(aRequest, Name)
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
            Form = await Api.FormCreate(aRequest, 'common/home')
            Res = await Form.Render()
        return Res

    def CreateApp(self, aRoutes: list = None, aErroMiddleware: dict = None) -> web.Application:
        App = super().CreateApp(aRoutes, aErroMiddleware)
        Loader = jinja2.FileSystemLoader(self._DirTpl)
        aiohttp_jinja2.setup(App, loader=Loader)
        return App

    async def RunApp(self):
        Log.Print(1, 'i', f'SrvView.RunApp() on port {self._SrvConf.port}')

        App = self.CreateApp(aErroMiddleware = {404: self._Err_404})
        await self.Run(App)
