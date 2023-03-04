# Created: 2021.02.26
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import re
from aiohttp import web
from multidict import MultiDict
#
from Inc.DataClass import DDataClass
from Inc.SrvWeb import TSrvBase, TSrvConf, FileReader
from IncP.Log import Log
from .Api import ApiView


@DDataClass
class TSrvViewConf(TSrvConf):
    dir_root: str = 'IncP/view'
    def_page: str = 'misc/info'
    home_page: str = 'common/home'
    deny: str = r'.tpl$|.py$'
    content_html: str = r'.html$'


class TSrvView(TSrvBase):
    def __init__(self, aSrvConf: TSrvViewConf):
        super().__init__(aSrvConf)
        self._SrvConf = aSrvConf

    def _GetDefRoutes(self) -> list:
        return [
            web.get('/api/{name:.*}', self._rApiGet),
            web.post('/api/{name:.*}', self._rApiPost),
            web.get('/{name:.*}', self._rIndex)
        ]

    async def _Form(self, aPath: str, aQuery: str = None, aPostData: MultiDict = None, aStatus: int = 200, aUserData: dict = None) -> web.Response:
        Data = await ApiView.Exec(aPath, aQuery, aPostData, aUserData)
        if ('err' in Data):
            Res = web.Response(text = Data['err'], content_type = 'text/html', status = Data['code'])
        else:
            Res = web.Response(text = Data['data'], content_type = 'text/html', status = aStatus)
        return Res

    async def _FormErr(self, aMsg: str, aStatus: int) -> web.Response:
        return await self._Form(
            aPath = self._SrvConf.def_page,
            aUserData = {'info': aMsg},
            aStatus = aStatus
        )

    async def _Err_404(self, aRequest: web.Request) -> web.Response:
        Path = aRequest.match_info.get('name')
        return await self._FormErr(f'Path not found {Path}', 404)

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
                    Res = await self._FormErr(f'Access denied {aRequest.path}', 403)
                elif (re.search(self._SrvConf.content_html, Name)):
                    with open(File, 'r', encoding='utf8') as F:
                        Data = F.read()
                    Res = web.Response(text = Data, content_type = 'text/html')
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
