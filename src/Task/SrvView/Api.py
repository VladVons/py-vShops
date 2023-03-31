# Created: 2021.02.28
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
from aiohttp import web
from multidict import MultiDict
#
from Inc.DataClass import DDataClass
from Inc.Misc.Cache import TCacheFile
from Inc.Misc.Jinja import TTemplate
from IncP.Plugins import TViewes
from IncP.ApiBase import TApiBase
from IncP.FormBase import TFormBase
from IncP.FormRender import TFormRender


@DDataClass
class TApiViewConf():
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

        self.Conf = TApiViewConf()
        self.Viewes: TViewes = None
        self.Tpl: TTemplate = None
        self.Cache: TCacheFileView = None

    def Init(self, aConf: dict):
        DirRoute = aConf['dir_route']
        self.Viewes = TViewes(DirRoute)
        self.InitLoader(aConf['loader'])

        Dirs = [
            f'{DirRoute}/{self.Conf.theme}/tpl',
            f'{DirRoute}/{self.Conf.theme_def}/tpl'
        ]
        SearchPath = [x for x in Dirs if (os.path.isdir(x))]
        assert (SearchPath), 'no tempate directories'
        self.Tpl = TTemplate(SearchPath)

        FormInfo = f'{DirRoute}/{self.Conf.theme_def}/tpl/{self.Conf.form_info}.{self.Tpl.Ext}'
        assert(os.path.isfile(FormInfo)), 'Default template not found'

        Cache = aConf['cache']
        Dir = Cache.get('path', 'Data/cache/view')
        os.makedirs(Dir, exist_ok = True)
        self.Cache = TCacheFileView(Dir, Cache.get('max_age', 5), Cache.get('incl_route'), Cache.get('excl_route'))
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

    async def _GetFormData(self, aRequest: web.Request, aRoute: str, aQuery: dict, aUserData: dict = None) -> dict:
        Form = self.GetForm(aRequest, aRoute)
        if (Form):
            if (aRoute != self.Conf.form_info):
                aQuery = dict(aQuery)

            if (aUserData is None):
                aUserData = {}
            Form.out.data = aUserData
            Form.out.route = aRoute

            Data = await Form.Render()
            Res = {'data': Data}
        else:
            Res = {'err': f'Route not found {aRoute}', 'code': 404}
        return Res

    async def GetFormData(self, aRequest: web.Request, aRoute: str, aQuery: dict, aUserData: dict = None) -> dict:
        #return await self._GetFormData(aRequest, aRoute, aQuery, aUserData)
        return await self.Cache.ProxyA(aRoute, aQuery, self._GetFormData, [aRequest, aRoute, aQuery, aUserData])

    async def ResponseFormInfo(self, aRequest: web.Request, aText: str, aStatus: int = 200) -> web.Response:
        if (self.Tpl.SearchModule(self.Conf.form_info)):
            Res = await self.ResponseForm(aRequest, self.Conf.form_info, aUserData = {'info': aText})
        else:
            Text = f'1) {aText}. 2) Info template {self.Conf.form_info} not found'
            Res = web.Response(text = Text, content_type = 'text/html', status = aStatus)
        Res.set_status(aStatus, aText)
        return Res

    async def ResponseFormHome(self, aRequest: web.Request) -> web.Response:
        return await self.ResponseForm(aRequest, self.Conf.form_home, aRequest.query)

    async def ResponseForm(self, aRequest: web.Request, aRoute: str, aQuery: MultiDict = None, aUserData: dict = None) -> web.Response:
        Data = await self.GetFormData(aRequest, aRoute, aQuery, aUserData)
        if ('err' in Data):
            if (aRoute == self.Conf.form_info):
                Res = web.Response(text = f'No default form {aRoute}', content_type = 'text/html')
            else:
                Res = await self.ResponseFormInfo(aRequest, Data['err'], Data['code'])
        else:
            Res = web.Response(text = Data['data'], content_type = 'text/html')
        return Res

    def LoadConf(self):
        Conf = self.GetConf()
        ApiConf = Conf['api_conf']
        self.Init(ApiConf)


ApiView = TApiView()
