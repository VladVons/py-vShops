# Created: 2021.02.28
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
from aiohttp import web
from jinja2 import Environment, BaseLoader
from jinja2.exceptions import TemplateNotFound
from jinja2.environment import Template
from multidict import MultiDict
#
from Inc.DataClass import DDataClass
from Inc.Misc.Cache import TCacheFile
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


class TCacheFileView(TCacheFile):
    def _GetAfter(self, _aPath: str, aData: object):
        if (aData):
            aData = {'data': aData}
        return aData

    def _SetBefore(self, _aPath: str, aData: object):
        if ('err' not in aData):
            return aData.get('data')


class TEnvironment(Environment):
    def join_path(self, template: str, parent: str):
        if (template.startswith('./')):
            Dir = parent.rsplit('/', maxsplit = 1)[0]
            template = f'{Dir}{template[1:]}'
        return template

    # def getitem(self, obj, argument: str):
    #     if (argument in obj):
    #         Res = obj.get(argument)
    #     else:
    #         Res = self.undefined(obj=obj, name=argument)
    #     return Res

    # def getattr(self, obj, attribute: str):
    #     if (hasattr(obj, attribute)):
    #         Res = getattr(obj, attribute)
    #     elif (attribute in obj):
    #         Res = obj.get(attribute)
    #     else:
    #         Res = self.undefined(obj=obj, name=attribute)
    #     return Res





class TFileSystemLoader(BaseLoader):
    def __init__(self, aSearchPath: list[str]):
        self.SearchPath = aSearchPath

    def get_source(self, environment: Environment, template: str):
        for Path in self.SearchPath:
            File = f'{Path}/{template}'
            if (os.path.isfile(File)):
                with open(File, 'r', encoding = 'utf-8') as F:
                    Data = F.read()

            MTime = os.path.getmtime(File)
            return (Data, File, lambda: MTime == os.path.getmtime(File))
        raise TemplateNotFound(template)

    def list_templates(self) -> list[str]:
        raise NotImplementedError()


class TApiView(TApiBase):
    def __init__(self):
        super().__init__()

        self.Conf = TApiViewConf()
        self.Viewes: TViewes = None
        self.TplEnv: Environment = None
        self.Cache: TCacheFileView = None

    def Init(self, aConf: dict):
        DirModule = aConf['dir_module']
        self.Viewes = TViewes(DirModule)
        self.InitLoader(aConf['loader'])

        Dirs = [
            f'{DirModule}/{self.Conf.theme}/tpl',
            f'{DirModule}/{self.Conf.theme_def}/tpl'
        ]
        SearchPath = [x for x in Dirs if (os.path.isdir(x))]
        assert (SearchPath), 'no tempate directories'
        Loader = TFileSystemLoader(SearchPath)
        self.TplEnv = TEnvironment(loader = Loader)

        FormInfo = f'{DirModule}/{self.Conf.theme_def}/tpl/{self.Conf.form_info}.tpl'
        assert(os.path.isfile(FormInfo)), 'Default template not found'

        Cache = aConf['cache']
        Dir = Cache.get('path', 'Data/cache/view')
        os.makedirs(Dir, exist_ok = True)
        self.Cache = TCacheFileView(Dir, Cache.get('max_age', 5), Cache.get('incl_module'), Cache.get('excl_module'))
        self.Cache.Clear()

    def GetForm(self, aRequest: web.Request, aModule: str) -> TFormBase:
        TplObj = self.GetTemplate(aModule)
        if (TplObj is None):
            return None

        Locate = [
            (TplObj.filename.rsplit('.', maxsplit=1)[0], 'TForm')
        ]

        for Module, Class in Locate:
            try:
                if (os.path.isfile(Module + '.py')):
                    Mod = __import__(Module.replace('/', '.'), None, None, [Class])
                    TClass = getattr(Mod, Class)
                    return TClass(self.Loader['ctrl'], aRequest, TplObj)
            except ModuleNotFoundError:
                pass
        return TFormRender(self.Loader['ctrl'], aRequest, TplObj)
        #raise ModuleNotFoundError(Locate[-1])

    async def _GetFormData(self, aRequest: web.Request, aModule: str, aQuery: dict, aUserData: dict = None) -> dict:
        Form = self.GetForm(aRequest, aModule)
        if (Form):
            if (aModule != self.Conf.form_info):
                aQuery = dict(aQuery)

            if (aUserData is None):
                aUserData = {}
            Form.out.data = aUserData
            Form.out.module = aModule

            Data = await Form.Render()
            Res = {'data': Data}
        else:
            Res = {'err': f'Module not found {aModule}', 'code': 404}
        return Res

    async def GetFormData(self, aRequest: web.Request, aModule: str, aQuery: dict, aUserData: dict = None) -> dict:
        #return await self._GetFormData(aRequest, aModule, aQuery, aUserData)
        return await self.Cache.ProxyA(aModule, aQuery, self._GetFormData, [aRequest, aModule, aQuery, aUserData])

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
            if (aModule == self.Conf.form_info):
                Res = web.Response(text = f'No default form {aModule}', content_type = 'text/html')
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
