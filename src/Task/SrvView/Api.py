# Created: 2021.02.28
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import json
from aiohttp import web
from aiohttp_session import get_session
#
from Inc.DataClass import DDataClass
from Inc.Misc.Cache import TCacheFile
from Inc.Misc.Jinja import TTemplate
from Inc.Var.Dict import GetDictDef
from Inc.SrvWeb.DDos import TIpLog
from IncP.ApiBase import TApiBase
from IncP.FormBase import TFormBase
from IncP.FormRender import TFormRender
from IncP.Log import Log
from IncP.Plugins import TViewes


@DDataClass
class TApiViewConf():
    loader: dict
    cache_route: dict = {}
    ip_log: dict = {}
    dir_route: str = 'MVC/catalog/view'
    dir_root: str = 'MVC/catalog/view'
    theme: str = 'theme1'
    theme_def: str = 'default'
    form_info: str = 'misc/info'
    form_home: str = 'common/home'
    form_module: str = 'module'
    request_scheme: str = 'https'
    force_redirect_to_seo: bool = False
    status_410: list = []


class TCacheFileView(TCacheFile):
    def _GetAfter(self, _aPath: str, aData: object):
        if (aData):
            aData = json.loads(aData)
        return aData

    def _SetBefore(self, _aPath: str, aData: object):
        if ('err' not in aData):
            return json.dumps(aData)


class TApiView(TApiBase):
    def __init__(self, aName: str):
        super().__init__()

        self.Name = aName
        Conf = self.GetConf()[aName]
        self.Conf = TApiViewConf(**Conf)
        self.Viewes = TViewes(self.Conf.dir_route)
        self.InitLoader(self.Conf.loader)

        Dirs = [
            f'{self.Conf.dir_route}/{self.Conf.theme}/tpl',
            f'{self.Conf.dir_route}/{self.Conf.theme_def}/tpl'
        ]
        SearchPath = [x for x in Dirs if (os.path.isdir(x))]
        assert(SearchPath), f'No tempate directories {Dirs}'
        self.Tpl = TTemplate(SearchPath)

        FormInfo = f'{self.Conf.dir_route}/{self.Conf.theme_def}/tpl/{self.Conf.form_info}.{self.Tpl.Ext}'
        assert(os.path.isfile(FormInfo)), f'Default template not found {FormInfo}'

        if (self.Conf.cache_route):
            Dir = self.Conf.cache_route.get('path', 'Data/cache/view')
            os.makedirs(Dir, exist_ok = True)
            Def = GetDictDef(self.Conf.cache_route, ['max_age', 'incl_route', 'excl_route'], [5, None, None])
            self.Cache = TCacheFileView(Dir, *Def)
            self.Cache.Clear()
        else:
            self.Cache = TCacheFileView('', aMaxAge = 0)

        self.IpLog = TIpLog(**self.Conf.ip_log)

    def GetForm(self, aRequest: web.Request, aRoute: str) -> TFormBase:
        if (aRoute.startswith('/')):
            return

        TplFile = self.Tpl.SearchModule(aRoute)
        if (not TplFile):
            return

        Locate = [
            (TplFile.rsplit('.', maxsplit=1)[0], 'TForm')
        ]

        for Module, Class in Locate:
            try:
                if (os.path.isfile(Module + '.py')):
                    Mod = __import__(Module.replace('/', '.'), None, None, [Class])
                    TClass = getattr(Mod, Class)
                    return TClass(self, aRequest)
            except ModuleNotFoundError:
                pass
        return TFormRender(self, aRequest)
        #raise ModuleNotFoundError(Locate[-1])

    async def _GetFormData(self, aRequest: web.Request, aQuery: dict) -> dict:
        Route = aQuery['route']
        Form = self.GetForm(aRequest, Route)
        if (Form):
            Form.out.route = Route
            Form.out.path = self.Name
            Form.out.query = aQuery
            Data = await Form.Render()
            Res = {
                'data': Data,
                'status_code': Form.out.get('status_code', 200),
                'status_value': Form.out.get('status_value'),
                'response': Form.out.get('response')
            }
        else:
            Res = {
                'err': f'Route not found {Route}',
                'status_code': 404
            }
        return Res

    async def GetFormData(self, aRequest: web.Request, aQuery: dict) -> dict:
        Route = aQuery['route']
        #return await self._GetFormData(aRequest, Route, aQuery, aUserData)
        return await self.Cache.ProxyA(Route, aQuery, self._GetFormData, [aRequest, aQuery])

    async def ResponseFormInfo(self, aRequest: web.Request, aText: str, aStatus: int = 200) -> web.Response:
        if (self.Tpl.SearchModule(self.Conf.form_info)):
            Res = await self.ResponseForm(aRequest, {'route': self.Conf.form_info, 'info': aText})
        else:
            Text = f'1) {aText}. 2) Info template {self.Conf.form_info} not found'
            Res = web.Response(text = Text, content_type = 'text/html', status = aStatus)
        Res.set_status(aStatus, aText)
        return Res

    async def ResponseFormHome(self, aRequest: web.Request) -> web.Response:
        Query = dict(aRequest.query)
        Query.update({'route': self.Conf.form_home})
        return await self.ResponseForm(aRequest, Query)

    async def ResponseErr(self, aRequest: web.Request, aErrCode = 404) -> web.Response:
        Query = {'route': self.Conf.form_info, 'raise_status_code': aErrCode}
        Data = await self.GetFormData(aRequest, Query)
        return web.Response(text = Data['data'], content_type = 'text/html', status = Data['status_code'])

    async def ResponseForm(self, aRequest: web.Request, aQuery: dict) -> web.Response:
        RemoteIp = aRequest.remote
        if (RemoteIp == '127.0.0.1'):
            RemoteIp = aRequest.headers.get('X-FORWARDED-FOR', '127.0.0.1')

        if (self.IpLog.Update(RemoteIp)):
            Data = await self.GetFormData(aRequest, aQuery)
            if ('err' in Data):
                return await self.ResponseErr(aRequest, 404)
        else:
            Msg = f'Too many connections. ip: {RemoteIp}'
            Log.Print(1, 'i', Msg)
            Data = {'status_code': 429, 'data': Msg}

        if (Data['status_code'] in [301, 302]):
            raise web.HTTPFound(location = Data['status_value'])
        elif (Data.get('response') is not None):
            return Data['response']
        else:
            return web.Response(text = Data['data'], content_type = 'text/html', status = Data['status_code'])

    async def ResponseApi(self, aRequest: web.Request) -> web.Response:
        Query = dict(aRequest.query)
        Session = await get_session(aRequest)
        Data = {
            '_path': self.Name,
            'host': aRequest.host,
            'method': Query.get('method', 'Main'),
            'path_qs': aRequest.path_qs,
            'path': aRequest.path,
            'query': Query,
            'session': dict(Session),
            'type': 'api'
        }

        Post = await aRequest.text()
        if (Post):
            try:
                Post = json.loads(Post)
                Data.update(Post)
            except ValueError:
                pass

        Ctrl = self.Loader['ctrl']
        Data = await Ctrl.Get(Query.get('route'), Data)

        Context = Query.get('context', 'json')
        if (Context == 'json'):
            Res = web.json_response(data = Data)
        else:
            Res = web.Response(text = Data)
        return Res

    async def GetSeoUrl(self, aMethod: str, aUrl: str) -> str:
        Data = {
            'type': 'api',
            'path': aUrl,
            'method': aMethod
        }
        Ctrl = self.Loader['ctrl']
        return await Ctrl.Get('seo', Data)

    async def GetSeoRedirect(self, aPath: str) -> str:
        Data = {
            'type': 'api',
            'method': 'Redirect',
            'path': aPath
        }
        Ctrl = self.Loader['ctrl']
        return await Ctrl.Get('seo', Data)

ApiViews = {Key: TApiView(Key) for Key in ['catalog', 'tenant']}
