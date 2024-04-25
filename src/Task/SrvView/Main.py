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
from .Api import ApiViews, TApiView


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

    async def _LoadFile(self, aRequest: web.Request, aApiView: TApiView) -> web.Response:
        Name = aRequest.match_info.get('name')
        File = f'{aApiView.Conf.dir_root}/{Name}'
        if (os.path.isfile(File)):
            if (re.search(self._SrvConf.deny, Name)):
                Res = await aApiView.ResponseFormInfo(aRequest, f'Access denied {aRequest.path}', 403)
            else:
                Res = self._GetMimeFile(File)
        else:
            Res = await self._Err_404(aRequest)
        return Res

    async def _rCatalog(self, aRequest: web.Request) -> web.Response:
        ApiView = ApiViews.get('catalog')
        assert(ApiView), f'unknown path `catalog` in {ApiViews.keys()}'

        Name = aRequest.match_info.get('name')
        NameExt = Name.rsplit('.', maxsplit=1)
        #if (Ext in ['js', 'css', 'jpg', 'png', 'ico', 'gif', 'txt', 'xml', 'woff2']):
        if (len(NameExt) == 2) and (2 <= len(NameExt) <= 5):
            Res = await self._LoadFile(aRequest, ApiView)
        else:
            if (ApiView.Conf.status_410):
                for xPattern in ApiView.Conf.status_410:
                    if (xPattern) and (not xPattern.startswith('-')):
                        Match = re.findall(xPattern, aRequest.path_qs)
                        if (Match):
                            return await ApiView.ResponseErr(aRequest, 410)
            if (Name):
                Url = await ApiView.GetSeoUrl('Decode', Name)
                Query = UrlDecode(Url)
                Query.update(aRequest.query)
                if (not Query):
                    return await ApiView.ResponseErr(aRequest, 404)
            else:
                if (ApiView.Conf.force_redirect_to_seo) and (aRequest.path_qs != '/'):
                    Url = await ApiView.GetSeoUrl('Encode', [aRequest.path_qs])
                    # prevent recursion
                    #if (Url[0].lstrip('/?') != aRequest.path_qs.lstrip('/?')):
                    if ('?' not in Url[0]):
                        raise web.HTTPFound(location = Url[0])
                Query = dict(aRequest.query)

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
        ApiView = ApiViews.get('tenant')
        assert(ApiView), f'unknown path `tenant` in {ApiViews.keys()}'

        Route = aRequest.query.get('route')
        if (Route):
            Session = await get_session(aRequest)
            AuthId = Session.get('auth_id')
            if (not AuthId):
                Query = {'route': 'common/login'}

            if (not Query.get('route')):
                Query.update({'route': ApiView.Conf.form_home})
            Res = await ApiView.ResponseForm(aRequest, Query)
        else:
            Res = await self._LoadFile(aRequest, ApiView)
        return Res

    async def RunApp(self):
        Log.Print(1, 'i', f'{self.__class__.__name__}.RunApp() on port {self._SrvConf.port}')

        ErroMiddleware = {404: self._Err_404, 'err_all': self._Err_All}
        App = self.CreateApp(aErroMiddleware = ErroMiddleware)

        #App['_conf_'] = 'MyConf'
        await self.Run(App)
