# Created: 2021.02.28
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
from aiohttp import web
#
from Inc.DataClass import DDataClass
from Inc.DictDef import TDictDef
from Inc.Misc.Cache import TCacheFile
from Inc.Misc.Jinja import TTemplate
from Inc.Util.Obj import GetDictDef
from IncP.Plugins import TViewes
from IncP.ApiBase import TApiBase
from IncP.FormBase import TFormBase
from IncP.FormRender import TFormRender


@DDataClass
class TApiViewConf():
    cache_route: dict
    loader: dict
    dir_route: str = 'MVC/catalog/view'
    dir_root: str = 'MVC/catalog/view'
    theme: str = 'theme1'
    theme_def: str = 'default'
    form_info: str = 'misc/info'
    form_home: str = 'common/home'
    form_module: str = 'module'


class TCacheFileView(TCacheFile):
    def _GetAfter(self, _aPath: str, aData: object):
        if (aData):
            aData = {'data': aData}
        return aData

    def _SetBefore(self, _aPath: str, aData: object):
        if ('err' not in aData):
            return aData.get('data')


class TApiView(TApiBase):
    def __init__(self):
        super().__init__()

        Conf = self.GetConf()
        self.Conf = TApiViewConf(**Conf)
        self.Viewes = TViewes(self.Conf.dir_route)
        self.InitLoader(self.Conf.loader)

        Dirs = [
            f'{self.Conf.dir_route}/{self.Conf.theme}/tpl',
            f'{self.Conf.dir_route}/{self.Conf.theme_def}/tpl'
        ]
        SearchPath = [x for x in Dirs if (os.path.isdir(x))]
        assert (SearchPath), 'no tempate directories'
        self.Tpl = TTemplate(SearchPath)

        FormInfo = f'{self.Conf.dir_route}/{self.Conf.theme_def}/tpl/{self.Conf.form_info}.{self.Tpl.Ext}'
        assert(os.path.isfile(FormInfo)), 'Default template not found'

        Dir = self.Conf.cache_route.get('path', 'Data/cache/view')
        os.makedirs(Dir, exist_ok = True)
        Def = GetDictDef(self.Conf.cache_route, ['max_age', 'incl_route', 'excl_route'], [5, None, None])
        self.Cache = TCacheFileView(Dir, *Def)
        self.Cache.Clear()

    def GetForm(self, aRequest: web.Request, aRoute: str) -> TFormBase:
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

    async def _GetFormData(self, aRequest: web.Request, aQuery: dict, aUserData: dict = None) -> dict:
        Route = aQuery['route']
        Form = self.GetForm(aRequest, Route)
        if (Form):
            if (Route == self.Conf.form_info):
                File = f'{Route}.{Form.Tpl.Ext}'
                Data = Form.Tpl.Render(File, aUserData)
            else:
                if (aUserData is None):
                    aUserData = {}
                Form.out.data = TDictDef('', aUserData)
                Form.out.route = Route
                Data = await Form.Render()
            Res = {'data': Data}
        else:
            Res = {'err': f'Route not found {Route}', 'code': 404}
        return Res

    async def GetFormData(self, aRequest: web.Request, aQuery: dict, aUserData: dict = None) -> dict:
        Route = aQuery['route']
        #return await self._GetFormData(aRequest, Route, aQuery, aUserData)
        return await self.Cache.ProxyA(Route, aQuery, self._GetFormData, [aRequest, aQuery, aUserData])

    async def ResponseFormInfo(self, aRequest: web.Request, aText: str, aStatus: int = 200) -> web.Response:
        if (self.Tpl.SearchModule(self.Conf.form_info)):
            Res = await self.ResponseForm(aRequest, {'route': self.Conf.form_info}, aUserData = {'info': aText})
        else:
            Text = f'1) {aText}. 2) Info template {self.Conf.form_info} not found'
            Res = web.Response(text = Text, content_type = 'text/html', status = aStatus)
        Res.set_status(aStatus, aText)
        return Res

    async def ResponseFormHome(self, aRequest: web.Request) -> web.Response:
        return await self.ResponseForm(aRequest, self.Conf.form_home, aRequest.query)

    async def ResponseForm(self, aRequest: web.Request, aQuery: dict, aUserData: dict = None) -> web.Response:
        Data = await self.GetFormData(aRequest, aQuery, aUserData)
        if ('err' in Data):
            Route = aQuery['route']
            if (Route == self.Conf.form_info):
                Res = web.Response(text = f'No default form {Route}', content_type = 'text/html')
            else:
                Res = await self.ResponseFormInfo(aRequest, Data['err'], Data['code'])
        else:
            Res = web.Response(text = Data['data'], content_type = 'text/html')
        return Res


ApiView = TApiView()
