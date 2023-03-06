# Created: 2021.02.26
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import re
from mimetypes import types_map
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
    form_def: str = 'misc/info'
    form_home: str = 'common/home'
    deny: str = r'.tpl$|.py$'


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

    async def _Form(self, aPath: str, aQuery: str = None, aPostData: MultiDict = None, aStatus: int = 200, aUserData: dict = None) -> web.Response:
        Data = await ApiView.Exec(aPath, aQuery, aPostData, aUserData)
        if ('err' in Data):
            Res = await self._FormMsg(Data['err'], Data['code'])
        else:
            Res = web.Response(text = Data['data'], content_type = 'text/html', status = aStatus)
        return Res

    async def _FormMsg(self, aMsg: str, aStatus: int) -> web.Response:
        return await self._Form(
            aPath = self._SrvConf.form_def,
            aUserData = {'info': aMsg},
            aStatus = aStatus
        )

    async def _Err_404(self, aRequest: web.Request) -> web.Response:
        Path = aRequest.match_info.get('name')
        return await self._FormMsg(f'Path not found {Path}', 404)

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
                    Res = await self._FormMsg(f'Access denied {aRequest.path}', 403)
                else:
                    Res = self._GetMimeFile(File)
            else:
                #Res = web.Response(text = f'File not found {Name}', status = 404)
                Res = await self._FormMsg(f'File not found {Name}', 404)
        else:
            Res = await self._Form(self._SrvConf.form_home, aRequest.query_string)
        return Res

    async def RunApp(self):
        Log.Print(1, 'i', f'SrvView.RunApp() on port {self._SrvConf.port}')

        ErroMiddleware = {404: self._Err_404}
        App = self.CreateApp(aErroMiddleware = ErroMiddleware)

        await self.Run(App)
