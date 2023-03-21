# Created: 2021.02.26
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import re
from mimetypes import types_map
from aiohttp import web
#
from Inc.DataClass import DDataClass
from Inc.SrvWeb import TSrvBase, TSrvConf, FileReader
from IncP.Log import Log
from .Api import ApiView


@DDataClass
class TSrvViewConf(TSrvConf):
    dir_root: str = 'MVC/main/MyDir'
    deny: str = r'.tpl$|.py$'


class TSrvView(TSrvBase):
    ''' web server for end user'''

    def __init__(self, aSrvConf: TSrvViewConf):
        super().__init__(aSrvConf)
        self._SrvConf = aSrvConf
        assert (os.path.isdir(self._SrvConf.dir_root)), 'Directory not exists'

    def _GetDefRoutes(self) -> list:
        return [
            web.get('/route/{name:.*}', self._rRoute),
            web.post('/route/{name:.*}', self._rRoute),
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

    @staticmethod
    async def _Err_404(aRequest: web.Request) -> web.Response:
        Path = aRequest.match_info.get('name')
        return await ApiView.ResponseFormInfo(aRequest, f'Path not found {Path}', 404)

    @staticmethod
    async def _Err_All(_aRequest: web.Request, aStack: dict) -> web.Response:
        Data = '\n<br>'.join(aStack)
        return web.Response(text = Data, content_type = 'text/html', status = 500)

    async def _rRoute(self, aRequest: web.Request) -> web.Response:
        Path = aRequest.match_info.get('name')
        return await ApiView.ResponseForm(aRequest, Path, aRequest.query)

    async def _rIndex(self, aRequest: web.Request) -> web.Response:
        Name = aRequest.match_info.get('name')
        if (Name):
            File = f'{self._SrvConf.dir_root}/{Name}'
            if (os.path.isfile(File)):
                if (re.search(self._SrvConf.deny, Name)):
                    Res = await ApiView.ResponseFormInfo(aRequest, f'Access denied {aRequest.path}', 403)
                else:
                    Res = self._GetMimeFile(File)
            else:
                Res = await ApiView.ResponseFormInfo(aRequest, f'File not found {Name}', 404)
        else:
            Res = await ApiView.ResponseFormHome(aRequest)
        return Res

    async def RunApp(self):
        Log.Print(1, 'i', f'SrvView.RunApp() on port {self._SrvConf.port}')

        ErroMiddleware = {404: self._Err_404}
        App = self.CreateApp(aErroMiddleware = ErroMiddleware)

        #App['_conf_'] = 'MyConf'
        await self.Run(App)
