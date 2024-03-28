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
from Inc.SrvWeb.Common import UrlDecode
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
            web.post('/tenant/api/{name:.*}', self._rApiTenant),
            web.post('/tenant/{name:.*}', self._rTenant),
            web.get('/tenant/{name:.*}', self._rTenant),

            web.post('/api/{name:.*}', self._rApiCatalog),
            web.get('/{name:.*}', self._rCatalog),
            web.post('/{name:.*}', self._rCatalog)
        ]

    async def _Route(self, aRequest: web.Request, aPath: str) -> web.Response:
        ApiView = ApiViews.get(aPath)
        assert(ApiView), f'unknown path `{aPath}` in {ApiViews.keys()}'

        Name = aRequest.match_info.get('name')
        Ext = Name.rsplit('.', maxsplit=1)[-1].lower()
        #if (Ext in ['js', 'css', 'jpg', 'png', 'ico', 'gif', 'txt', 'xml', 'woff2']):
        if (Ext and len(Ext) <= 5):
            File = f'{ApiView.Conf.dir_root}/{Name}'
            if (os.path.isfile(File)):
                if (re.search(self._SrvConf.deny, Name)):
                    Res = await ApiView.ResponseFormInfo(aRequest, f'Access denied {aRequest.path}', 403)
                else:
                    Res = self._GetMimeFile(File)
            else:
                Res = await self._Err_404(aRequest)
        else:
            if (Name):
                Url = await ApiView.GetSeoUrl('Decode', Name)
                Query = UrlDecode(Url)
            else:
                Query = dict(aRequest.query)

            if (aPath == 'tenant'):
                Session = await get_session(aRequest)
                AuthId = Session.get('auth_id')
                if (not AuthId):
                    Query = {'route': 'common/login'}

            if (not Query.get('route')):
                Query.update({'route': ApiView.Conf.form_home})
            Res = await ApiView.ResponseForm(aRequest, Query)
        return Res

    @staticmethod
    async def _Err_404(aRequest: web.Request) -> web.Response:
        Path = aRequest.match_info.get('name')
        return await ApiViews['catalog'].ResponseFormInfo(aRequest, f'Path not found {Path}', 404)

    @staticmethod
    async def _Err_All(_aRequest: web.Request, aStack: dict) -> web.Response:
        Data = '\n<br>'.join(aStack)
        return web.Response(text = Data, content_type = 'text/html', status = 500)

    async def _rApiTenant(self, aRequest: web.Request) -> web.Response:
        return await ApiViews['tenant'].ResponseApi(aRequest)

    async def _rApiCatalog(self, aRequest: web.Request) -> web.Response:
        return await ApiViews['catalog'].ResponseApi(aRequest)

    async def _rTenant(self, aRequest: web.Request) -> web.Response:
        return await self._Route(aRequest, 'tenant')

    async def _rCatalog(self, aRequest: web.Request) -> web.Response:
        return await self._Route(aRequest, 'catalog')

    async def RunApp(self):
        Log.Print(1, 'i', f'SrvView.RunApp() on port {self._SrvConf.port}')

        ErroMiddleware = {404: self._Err_404, 'err_all': self._Err_All}
        App = self.CreateApp(aErroMiddleware = ErroMiddleware)

        #App['_conf_'] = 'MyConf'
        await self.Run(App)
