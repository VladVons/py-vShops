# Created: 2021.02.28
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
from aiohttp import web
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound
from jinja2.environment import Template
from multidict import MultiDict
#
from Inc.DataClass import DDataClass
from IncP.Plugins import TViewes
from IncP.ApiBase import TApiBase
from IncP.FormBase import TFormBase


@DDataClass
class TApiViewConf():
    theme: str = 'theme1'
    theme_def: str = 'default'
    form_info: str = 'misc/info'
    form_home: str = 'common/home'


class TApiView(TApiBase):
    def __init__(self):
        super().__init__()

        self.Conf = TApiViewConf()
        self.Viewes: TViewes = None
        self.TplEnv: Environment = None

    def Init(self, aConf: dict):
        DirModule = aConf['dir_module']
        self.Viewes = TViewes(DirModule)
        self.InitLoader(aConf['api'])

        Loader = FileSystemLoader(
            searchpath = [
                f'{DirModule}/{self.Conf.theme}/tpl',
                f'{DirModule}/{self.Conf.theme_def}/tpl'
            ]
        )
        self.TplEnv = Environment(loader = Loader)

    def GetForm(self, aRequest: web.Request, aModule: str) -> TFormBase:
        TplObj = self.GetTemplate(aModule)
        if (TplObj is None):
            return None

        Locate = [
            (TplObj.filename.rsplit('.', maxsplit=1)[0], 'TForm'),
            (f'{self.Viewes.Dir}/ctrl/{aModule}', 'TForm'),
            ('IncP/FormBase', 'TFormBase')
        ]

        for Module, Class in Locate:
            try:
                if (os.path.isfile(Module + '.py')):
                    Mod = __import__(Module.replace('/', '.'), None, None, [Class])
                    TClass = getattr(Mod, Class)
                    return TClass(self.Loader['ctrl'], aRequest, TplObj)
            except ModuleNotFoundError:
                pass
        return None

    async def GetFormData(self, aRequest: web.Request, aModule: str, aQuery: dict, aUserData: dict = None) -> dict:
        Form = self.GetForm(aRequest, aModule)
        if (Form):
            if (aModule != self.Conf.form_info):
                aQuery = dict(aQuery)

            if (aUserData is None):
                aUserData = {}
            Form.out.data.SetData(aUserData)
            Form.out.module = aModule

            Data = await Form.Render()
            Res = {'data': Data}
        else:
            Res = {'err': f'Module not found {aModule}', 'code': 404}
        return Res

    def GetTemplate(self, aModule: str) -> Template:
        try:
            Res = self.TplEnv.get_template(f'{aModule}.tpl')
        except TemplateNotFound:
            Res = None
        return Res

    async def ResponseFormInfo(self, aRequest: web.Request, aText: str, aStatus: int = 200) -> web.Response:
        TplObj = self.GetTemplate(self.Conf.form_info)
        if (TplObj):
            Res = await self.ResponseForm(aRequest, self.Conf.form_info, aUserData = {'info': aText})
        else:
            Text = f'1) {aText}. 2) Info template {self.Conf.form_info} not found'
            Res = web.Response(text = Text, content_type = 'text/html', status = aStatus)
        Res.set_status(aStatus, aText)
        return Res

    async def ResponseFormHome(self, aRequest: web.Request) -> web.Response:
        return await self.ResponseForm(aRequest, self.Conf.form_home, aRequest.query)

    async def ResponseForm(self, aRequest: web.Request, aModule: str, aQuery: MultiDict = None, aUserData: dict = None) -> web.Response:
        Data = await self.GetFormData(aRequest, aModule, aQuery, aUserData)
        if ('err' in Data):
            Res = await self.ResponseFormInfo(aRequest, Data['err'], Data['code'])
        else:
            Res = web.Response(text = Data['data'], content_type = 'text/html')
        return Res

    def LoadConf(self):
        Conf = self.GetConf()
        ApiConf = Conf['api_conf']
        self.Init(ApiConf)


ApiView = TApiView()
