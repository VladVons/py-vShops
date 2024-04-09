# Created: 2023.02.20
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import time
from aiohttp import web
#
from Inc.Misc.Misc import TJsonEncoder
from Inc.SrvWeb.SrvBase import TSrvBase
from IncP.Log import Log
from .Api import ApiCtrls


class TSrvCtrl(TSrvBase):
    def _GetDefRoutes(self) -> list:
        return [
            web.get('/route/{name:.*}', self._rRoute),
            web.post('/route/{name:.*}', self._rRoute)
        ]

    async def _rRoute(self, aRequest: web.Request) -> web.Response:
        TimeStart = time.time()
        Name = aRequest.match_info.get('name')
        if (not self._CheckRequestAuth(aRequest)):
            Status = 403
            Res = {'err': 'Authorization failed'}
        else:
            Status = 200
            Data = await aRequest.json()
            Path = Data.get('_path')
            if (Path in ApiCtrls):
                Res = await ApiCtrls[Path].Exec(Name, Data)
            else:
                Res = {'err': f'unknown _path `{Path}`'}

        if (Data.get('type') != 'api'):
            Res['info'] = {
                'module': Name,
                'method': aRequest.query.get('method', 'Main'),
                'time': round(time.time() - TimeStart, 4),
                'status': Status
            }
        return web.json_response(Res, status = Status, dumps=TJsonEncoder.Dumps)

    @staticmethod
    async def _Err_404(aRequest: web.Request) -> web.Response:
        Data = {'err': f'unknown path {aRequest.path}', 'class': __file__}
        return web.json_response(Data, status = 404)

    @staticmethod
    async def _Err_All(_aRequest: web.Request, aStack: list) -> web.Response:
        return web.json_response({'err': aStack}, status = 500)

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

        #from Task.SrvModel.Api import ApiModel
        #await ApiModel.AEvent.wait()
        #await ApiCtrl.ExecOnce()
