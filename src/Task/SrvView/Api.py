# Created: 2021.02.28
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound
from multidict import MultiDict
#
from Inc.DataClass import DDataClass
from IncP.Plugins import TViewes
from IncP.ApiBase import TApiBase, TApiConf


@DDataClass
class TApiViewConf(TApiConf):
    dir_3w: str = 'view'
    dir_tpl: str = 'IncP/view'
    dir_root: str = 'Task/SrvView'
    tpl_ext: str = '.tpl'
    def_page: str = 'info'
    theme: str = 'theme1'


class TApiView(TApiBase):
    def __init__(self):
        super().__init__()
        self.Viewes: TViewes = None
        self.TplEnv: Environment = None

    def Init(self, aConf: TApiViewConf):
        self.Conf = aConf
        self.Conf.dir_module = 'IncP/view'
        self.Viewes = TViewes(self.Conf.dir_module)
        self.InitMaster()

        Loader = FileSystemLoader(
            searchpath = [
                f'{self.Conf.dir_module}/{self.Conf.theme}/tpl',
                f'{self.Conf.dir_module}/default/tpl'
            ]
        )
        self.TplEnv = Environment(loader = Loader)

    async def Exec(self, aModule: str, aQuery: str, aPostData: MultiDict = None, aUserData: dict = None) -> dict:
        MasterData = await self.Master.Get(aModule, aQuery)
        try:
            Template = self.TplEnv.get_template(aModule + self.Conf.tpl_ext)
        except TemplateNotFound as E:
            return {'err': f'Template not found {E}', 'code': 404}

        FilePy = Template.filename.replace('/tpl/', '/py/').rstrip('.tpl')
        Locate = [
            (FilePy, 'TForm'),
            ('IncP/FormBase', 'TFormBase')
        ]

        TClass = None
        for Module, Class in Locate:
            try:
                if (os.path.isfile(Module + '.py')):
                    Mod = __import__(Module.replace('/', '.'), None, None, [Class])
                    TClass = getattr(Mod, Class)
                    break
            except ModuleNotFoundError as _E:
                pass

        if (TClass):
            Form = TClass(aModule, aQuery, aPostData, Template, MasterData, aUserData)
            Data = await Form.Render()
            Res = {'data': Data}
        else:
            Res = {'err': f'Module not found {aModule}', 'code': 404}
        return Res

    def LoadConf(self):
        Conf = self.GetConf()
        ApiConf = Conf['api_conf']
        self.Init(TApiViewConf(**ApiConf))

ApiView = TApiView()
