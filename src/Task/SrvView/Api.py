# Created: 2021.02.28
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
from aiohttp import web
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound
from multidict import MultiDict
#
from Inc.DataClass import DDataClass
from IncP.Plugins import TViewes
from IncP.ApiBase import TApiBase, TApiConf
from IncP.FormBase import TFormBase


@DDataClass
class TApiViewConf(TApiConf):
    theme: str = 'theme1'
    theme_def: str = 'default'
    form_info: str = 'misc/info'
    form_home: str = 'common/home'


class TApiView(TApiBase):
    def __init__(self):
        super().__init__()
        self.Viewes: TViewes = None
        self.TplEnv: Environment = None

    def Init(self, aConf: TApiViewConf):
        self.Conf = aConf
        self.Viewes = TViewes(self.Conf.dir_module)
        self.InitMaster()

        Loader = FileSystemLoader(
            searchpath = [
                f'{self.Conf.dir_module}/{self.Conf.theme}/tpl',
                f'{self.Conf.dir_module}/{self.Conf.theme_def}/tpl'
            ]
        )
        self.TplEnv = Environment(loader = Loader)

    def GetForm(self, aRequest: web.Request, aModule: str) -> TFormBase:
        try:
            Template = self.TplEnv.get_template(f'{aModule}.tpl')
        except TemplateNotFound:
            return None

        Locate = [
            (Template.filename.rsplit('.', maxsplit=1)[0], 'TForm'),
            (f'{self.Conf.dir_module}/ctrl/{aModule}', 'TForm'),
            ('IncP/FormBase', 'TFormBase')
        ]

        for Module, Class in Locate:
            try:
                if (os.path.isfile(Module + '.py')):
                    Mod = __import__(Module.replace('/', '.'), None, None, [Class])
                    TClass = getattr(Mod, Class)
                    return TClass(aRequest, Template)
            except ModuleNotFoundError:
                pass
        return None

    async def GetFormData(self, aRequest: web.Request, aModule: str, aQuery: dict, aUserData: dict = None) -> dict:
        Form = self.GetForm(aRequest, aModule)
        if (Form):
            if (aModule != self.Conf.form_info):
                DataApi = await self.Master.Get(aModule, aQuery)
                Form.out.data_api = DataApi

            if (aUserData is None):
                aUserData = {}
            Form.out.data.SetData(aUserData)

            Data = await Form.Render()
            Res = {'data': Data}
        else:
            Res = {'err': f'Module not found {aModule}', 'code': 404}
        return Res

    async def ResponseFormInfo(self, aRequest: web.Request, aText: str, aStatus: int = 200) -> web.Response:
        Res = await self.ResponseForm(aRequest, self.Conf.form_info, {'info': aText})
        Res.set_status(aStatus, aText)
        return Res

    async def ResponseFormHome(self, aRequest: web.Request) -> web.Response:
        return await self.ResponseForm(aRequest, self.Conf.form_home, aRequest.query)

    async def ResponseForm(self, aRequest: web.Request, aModule: str, aQuery: MultiDict, aUserData: dict = None) -> web.Response:
        Data = await self.GetFormData(aRequest, aModule, dict(aQuery), aUserData)
        if ('err' in Data):
            Res = web.Response(text = Data['err'], content_type = 'text/html', status = Data['code'])
            #Res = await self._FormMsg(Data['err'], Data['code'])
        else:
            Res = web.Response(text = Data['data'], content_type = 'text/html')
        return Res

    def LoadConf(self):
        Conf = self.GetConf()
        ApiConf = Conf['api_conf']
        self.Init(TApiViewConf(**ApiConf))


ApiView = TApiView()
