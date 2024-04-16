# Created: 2023.02.20
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
from aiohttp import web
#
from Inc.SrvWeb.SrvBase import TSrvConf
from IncP.Log import Log
from IncP.SrvBaseEx import TSrvBaseEx
from .Api import ApiImg


class TSrvImg(TSrvBaseEx):
    def __init__(self, aSrvConf: TSrvConf):
        super().__init__(aSrvConf)
        assert(os.path.isdir(ApiImg.Conf.dir_root)), f'Directory not exists {ApiImg.Conf.dir_root}'

    def _GetDefRoutes(self) -> list:
        return [
            web.post('/api/{name:.*}', self._rApi),
            web.get('/img/{name:.*}', self._rImg)
        ]

    async def _rImg(self, aRequest: web.Request) -> web.Response:
        Name = aRequest.match_info.get('name')
        File = f'{ApiImg.Conf.dir_root}/{Name}'
        if (os.path.isfile(File)):
            Res = self._GetMimeFile(File)
        else:
            Res = web.Response(text = 'File not found', content_type = 'text/html', status = 404)
        return Res

    @staticmethod
    async def _Err_404(aRequest: web.Request) -> web.Response:
        Data = f'unknown path {aRequest.path}'
        return web.Response(text = Data, content_type = 'text/html', status = 404)

    @staticmethod
    async def _Err_All(_aRequest: web.Request, aStack: list) -> web.Response:
        return web.json_response({'err': aStack}, status = 500)

    def GetApi(self, _aPath: str) -> object:
        return ApiImg

    async def RunApp(self):
        Log.Print(1, 'i', f'{self.__class__.__name__}.RunApp() on port {self._SrvConf.port}')

        ErroMiddleware = {
            404: self._Err_404,
            'err_all': self._Err_All
        }
        App = self.CreateApp(aErroMiddleware = ErroMiddleware)
        await self.Run(App)

    async def RunApi(self):
        Log.Print(1, 'i', f'{self.__class__.__name__}.RunApi() only')
