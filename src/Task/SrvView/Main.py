# Created: 2021.02.26
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import re
from aiohttp import web
#
from Inc.DataClass import DDataClass
from Inc.SrvWeb import TSrvBase, TSrvConf
from IncP.Log import Log
from .Api import ApiView


@DDataClass
class TSrvViewConf(TSrvConf):
    deny: str = r'.j2$|.py$'


class TSrvView(TSrvBase):
    ''' web server for end user'''

    def __init__(self, aSrvConf: TSrvViewConf):
        super().__init__(aSrvConf)
        self._SrvConf = aSrvConf
        assert(os.path.isdir(ApiView.Conf.dir_root)), f'Directory not exists {ApiView.Conf.dir_root}'

    def _GetDefRoutes(self) -> list:
        return [
            web.get('/{name:.*}', self._rIndex),
            web.post('/api/{name:.*}', self._rApi)
        ]

    @staticmethod
    async def _Err_404(aRequest: web.Request) -> web.Response:
        Path = aRequest.match_info.get('name')
        return await ApiView.ResponseFormInfo(aRequest, f'Path not found {Path}', 404)

    @staticmethod
    async def _Err_All(_aRequest: web.Request, aStack: dict) -> web.Response:
        Data = '\n<br>'.join(aStack)
        return web.Response(text = Data, content_type = 'text/html', status = 500)

    async def _rApi(self, aRequest: web.Request) -> web.Response:
        return await ApiView.ResponseApi(aRequest)

    async def _rIndex(self, aRequest: web.Request) -> web.Response:
        Name = aRequest.match_info.get('name')
        Route = aRequest.query.get('route')
        if (Route):
            Res = await ApiView.ResponseForm(aRequest, dict(aRequest.query))
        elif (not Name):
            Res = await ApiView.ResponseForm(aRequest, {'route': ApiView.Conf.form_home})
        else:
            File = f'{ApiView.Conf.dir_root}/{Name}'
            if (os.path.isfile(File)):
                if (re.search(self._SrvConf.deny, Name)):
                    Res = await ApiView.ResponseFormInfo(aRequest, f'Access denied {aRequest.path}', 403)
                else:
                    Res = self._GetMimeFile(File)
            else:
                Res = await self._Err_404(aRequest)
        return Res

    async def RunApp(self):
        Log.Print(1, 'i', f'SrvView.RunApp() on port {self._SrvConf.port}')

        ErroMiddleware = {404: self._Err_404, 'err_all': self._Err_All}
        App = self.CreateApp(aErroMiddleware = ErroMiddleware)

        #App['_conf_'] = 'MyConf'
        await self.Run(App)
