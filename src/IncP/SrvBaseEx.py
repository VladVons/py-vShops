# Created: 2024.04.03
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import time
from aiohttp import web
#
from Inc.Misc.Misc import TJsonEncoder
from Inc.SrvWeb.SrvBase import TSrvBase


class TSrvBaseEx(TSrvBase):
    def _GetDefRoutes(self) -> list:
        raise NotImplementedError()

    def GetApi(self) -> object:
        raise NotImplementedError()

    @staticmethod
    async def _Err_404(aRequest: web.Request) -> web.Response:
        Data = {'err': f'unknown path {aRequest.path}', 'class': __file__}
        return web.json_response(Data, status = 404)

    @staticmethod
    async def _Err_All(_aRequest: web.Request, aStack: list) -> web.Response:
        return web.json_response({'err': aStack}, status = 500)

    async def _rApi(self, aRequest: web.Request) -> web.Response:
        Res = {}
        TimeStart = time.time()
        Name = aRequest.match_info.get('name')
        if (not self._CheckRequestAuth(aRequest)):
            Status = 403
            Res['err'] = 'Authorization failed'
        else:
            Status = 200
            DataIn = await aRequest.json()
            Api = self.GetApi()
            DataOut = await Api.Exec(Name, DataIn)
            if (isinstance(DataOut, dict)) and ('err' in DataOut):
                Res = DataOut
            else:
                Res['data'] = DataOut

        Res['info'] = {
            'time': round(time.time() - TimeStart, 4),
            'status': Status
        }
        return web.json_response(Res, status = Status, dumps=TJsonEncoder.Dumps)
