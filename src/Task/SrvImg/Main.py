# Created: 2023.02.20
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import time
from aiohttp import web
#
from Inc.SrvWeb.SrvBase import TSrvBase, TSrvConf
from IncP.Log import Log
from .Api import ApiImg


class TSrvImg(TSrvBase):
    def __init__(self, aSrvConf: TSrvConf):
        super().__init__(aSrvConf)
        assert(os.path.isdir(ApiImg.Conf.dir_root)), f'Directory not exists {ApiImg.Conf.dir_root}'

    def _GetDefRoutes(self) -> list:
        return [
            web.post('/api/{name:.*}', self._rApi),
            web.get('/img/{name:.*}', self._rImg)
        ]

    async def _rApi(self, aRequest: web.Request) -> web.Response:
        TimeStart = time.time()
        Name = aRequest.match_info.get('name')
        if (not self._CheckRequestAuth(aRequest)):
            Status = 403
            Res = {'err': 'Authorization failed'}
        else:
            Status = 200
            Data = await aRequest.json()
            Res = await ApiImg.Exec(Name, Data)

        Res['info'] = {
            'module': Name,
            'method': aRequest.query.get('method', 'Main'),
            'count': ApiImg.ExecCnt,
            'time': round(time.time() - TimeStart, 4),
            'status': Status
        }
        return web.json_response(Res, status = Status)

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

    async def RunApp(self):
        Log.Print(1, 'i', f'SrvImg.RunApp() on port {self._SrvConf.port}')

        ErroMiddleware = {
            404: self._Err_404,
            'err_all': self._Err_All
        }
        App = self.CreateApp(aErroMiddleware = ErroMiddleware)
        await self.Run(App)

    async def RunApi(self):
        Log.Print(1, 'i', 'SrvImg.RunApi() only')
