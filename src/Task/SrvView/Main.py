# Created: 2021.02.26
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

# https://github.com/aio-libs/aiohttp
# https://docs.aiohttp.org/en/stable/web_advanced.html#aiohttp-web-app-runners


import os
import re
from aiohttp import web
from multidict import MultiDict
#
from Inc.DataClass import DDataClass
from Inc.SrvWeb import TSrvBase, TSrvConf, FileReader
from IncP.Log import Log
from .Api import Api


@DDataClass
class TSrvViewConf(TSrvConf):
    dir_root: str = 'Task/SrvView'
    def_page: str = 'misc/info'
    home_page: str = 'common/home'
    deny: str = r'.tpl$|.py$'
    allow: str = r'.html$'


class TSrvView(TSrvBase):
    def __init__(self, aSrvConf: TSrvViewConf):
        super().__init__(aSrvConf)
        self._SrvConf = aSrvConf

    def _GetDefRoutes(self) -> list:
        return [
            web.get('/api/{name:.*}', self._rApiGet),
            web.post('/api/{name:.*}', self._rApiPost),
            web.get('/{name:.*}', self._rIndex),
            web.post('/{name:.*}', self._rIndex),
        ]

    async def _Form(self, aPath: str, aQuery: str, aPostData: MultiDict = None, aStatus: int = 200) -> web.Response:
        Text = await Api.Exec(aPath, aQuery, aPostData)
        return web.Response(text = Text, content_type = 'text/html', status = aStatus)

    async def _Err_404(self, aRequest: web.Request) -> web.Response:
        return await self._Form(self._SrvConf.def_page, MultiDict({}), f'Path not found {aRequest.path}', 404)

    async def _rApiGet(self, aRequest: web.Request) -> web.Response:
        Path = aRequest.match_info.get('name')
        return await self._Form(Path, aRequest.query_string, None)

    async def _rApiPost(self, aRequest: web.Request) -> web.Response:
        Path = aRequest.match_info.get('name')
        Post = await aRequest.post()
        return await self._Form(Path, aRequest.query_string, Post)

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
                Res = web.Response(text = f'File not found {Name}', status = 404)
        else:
            Res = await self._Form(self._SrvConf.home_page, aRequest.query_string)
        return Res

    async def RunApp(self):
        Log.Print(1, 'i', f'SrvView.RunApp() on port {self._SrvConf.port}')

        ErroMiddleware = {404: self._Err_404}
        App = self.CreateApp(aErroMiddleware = ErroMiddleware)

        await self.Run(App)
