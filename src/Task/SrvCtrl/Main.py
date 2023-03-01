# Created: 2023.02.20
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import time
from aiohttp import web
#
from Inc.SrvWeb.SrvBase import TSrvBase, TSrvConf
from Inc.DataClass import DDataClass
from Inc.Misc.Request import TRequestJson, TAuth
from IncP.Log import Log
from .Api import Api


@DDataClass
class TSrvCtrlConf(TSrvConf):
    # user: str
    # password: str
    model_user: str
    model_password: str
    model_api: str = 'http://localhost/api'


class TSrvCtrl(TSrvBase):
    def __init__(self, aSrvConf: TSrvCtrlConf):
        super().__init__(aSrvConf)
        self._SrvConf = aSrvConf

        Auth = TAuth(self._SrvConf.model_user, self._SrvConf.model_password)
        self.RequestModel = TRequestJson(aAuth=Auth)

    def _GetDefRoutes(self) -> list:
        return [
            web.get('/api/{name:.*}', self._rApi),
            web.post('/api/{name:.*}', self._rApi)
        ]

    async def _rApi(self, aRequest: web.Request) -> web.Response:
        Res = {}

        TimeStart = time.time()
        if (not self._CheckAuthRequest(aRequest)):
            Status = 403
            Res['err'] = 'Authorization failed'
        else:
            Status = 200
            Name = aRequest.match_info.get('name')
            Url = f'{self._SrvConf.model_api}/{Name}?{aRequest.query_string}'
            Res['data'] = await self.RequestModel.Send(Url, {})
        Res['time'] = round(time.time() - TimeStart, 4)
        return web.json_response(Res, status = Status)

    @staticmethod
    async def _Err_404(aRequest: web.Request) -> web.Response:
        Data = {'err': f'unknown path {aRequest.path}'}
        return web.json_response(Data, status = 404)

    async def RunApp(self):
        Log.Print(1, 'i', f'SrvCtrl.RunApp() on port {self._SrvConf.port}')

        App = self.CreateApp(aErroMiddleware = {404: self._Err_404})
        await self.Run(App)
