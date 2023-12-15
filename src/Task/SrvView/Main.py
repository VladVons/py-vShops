# Created: 2021.02.26
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import os
import re
from aiohttp import web
from aiohttp_session import get_session
#
from Inc.DataClass import DDataClass
from Inc.SrvWeb import TSrvBase, TSrvConf
from IncP.Log import Log
from .Api import ApiViews


@DDataClass
class TSrvViewConf(TSrvConf):
    deny: str = r'.j2$|.py$'


class TSrvView(TSrvBase):
    ''' web server for end user'''

    def __init__(self, aSrvConf: TSrvViewConf):
        super().__init__(aSrvConf)
        self._SrvConf = aSrvConf
        #-x1 assert(os.path.isdir(ApiView.Conf.dir_root)), f'Directory not exists {ApiView.Conf.dir_root}'

    def _GetDefRoutes(self) -> list:
        return [
            web.post('/api/admin{name:.*}', self._rApiAdmin),
            web.post('/api/{name:.*}', self._rApiCatalog),
            web.get('/admin{name:.*}', self._rAdmin),
            web.post('/admin{name:.*}', self._rAdmin),
            web.get('/{name:.*}', self._rCatalog)
        ]

    async def _Route(self, aRequest: web.Request, aPath: str) -> web.Response:
        ApiView = ApiViews.get(aPath)
        assert(ApiView), f'unknown path `{aPath}` in {ApiViews.keys()}'

        Name = aRequest.match_info.get('name')
        if (Name in ['/', '']):
            Query = dict(aRequest.query)
            if (aPath == 'admin'):
                Session = await get_session(aRequest)
                UserId = Session.get('user_id')
                if (not UserId):
                    Query = {'route': 'common/login'}

            if (not Query.get('route')):
                Query.update({'route': ApiView.Conf.form_home})
            Res = await ApiView.ResponseForm(aRequest, Query)
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

    @staticmethod
    async def _Err_404(aRequest: web.Request) -> web.Response:
        Path = aRequest.match_info.get('name')
        return await ApiViews['catalog'].ResponseFormInfo(aRequest, f'Path not found {Path}', 404)

    @staticmethod
    async def _Err_All(_aRequest: web.Request, aStack: dict) -> web.Response:
        Data = '\n<br>'.join(aStack)
        return web.Response(text = Data, content_type = 'text/html', status = 500)

    async def _rApiAdmin(self, aRequest: web.Request) -> web.Response:
        return await ApiViews['admin'].ResponseApi(aRequest)

    async def _rApiCatalog(self, aRequest: web.Request) -> web.Response:
        return await ApiViews['catalog'].ResponseApi(aRequest)

    async def _rAdmin(self, aRequest: web.Request) -> web.Response:
        return await self._Route(aRequest, 'admin')

    async def _rCatalog(self, aRequest: web.Request) -> web.Response:
        return await self._Route(aRequest, 'catalog')

    async def RunApp(self):
        Log.Print(1, 'i', f'SrvView.RunApp() on port {self._SrvConf.port}')

        ErroMiddleware = {404: self._Err_404, 'err_all': self._Err_All}
        App = self.CreateApp(aErroMiddleware = ErroMiddleware)

        #App['_conf_'] = 'MyConf'
        await self.Run(App)
