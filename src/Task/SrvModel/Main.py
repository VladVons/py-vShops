# Created: 2023.02.20
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import time
from aiohttp import web
#
from Inc.DataClass import DDataClass
from Inc.Sql.ADb import TDbAuth
from Inc.SrvWeb.SrvBase import TSrvBase, TSrvConf
from IncP.Log import Log
from .Api import Api


@DDataClass
class TSrvDbConf(TSrvConf):
    # user: str
    # password: str
    pass


class TSrvDb(TSrvBase):
    def __init__(self, aSrvConf: TSrvDbConf, aDbConf: TDbAuth):
        super().__init__(aSrvConf)
        self._SrvConf = aSrvConf
        self._DbConf = aDbConf

    async def _rApi(self, aRequest: web.Request) -> web.Response:
        Res = {}

        TimeStart = time.time()
        Name = aRequest.match_info.get('name')
        if (not self._CheckAuthRequest(aRequest)):
            Status = 403
            Res['err'] = 'Authorization failed'
        else:
            Status = 200
            Res = await self._GetPostData(aRequest)
            Method = Res.get('method')
            if ('err' not in Res):
                Res = await Api.Exec(Name, Res)

        Res['info'] = {
            'module': Name,
            'method': Method,
            'query': Api.QueryCnt,
            'time': round(time.time() - TimeStart, 4)
        }
        return web.json_response(Res, status=Status)

    async def _cbOnStartup(self, aApp: web.Application):
        #aApp['conf'] = self.Conf

        try:
            await Api.DbInit(self._DbConf)
            yield
            # wait till working...
        except Exception as E:
            Log.Print(1, 'x', '_cbOnStartup()', aE = E)
        finally:
            Log.Print(1, 'i', '_cbOnStartup(). Close connection')
            await Api.DbClose()

    def _GetDefRoutes(self) -> list:
        return [
            web.get('/api/{name:.*}', self._rApi),
            web.post('/api/{name:.*}', self._rApi),
            web.post('/api', self._rApi)
        ]

    @staticmethod
    async def _Err_404(aRequest: web.Request) -> web.Response:
        Data = {'err': f'unknown path {aRequest.path}'}
        return web.json_response(Data, status = 404)

    async def RunApp(self):
        Log.Print(1, 'i', f'SrvDb.RunApp() on port {self._SrvConf.port}')

        App = self.CreateApp(aErroMiddleware = {404: self._Err_404})
        App.cleanup_ctx.append(self._cbOnStartup)

        await self.Run(App)
