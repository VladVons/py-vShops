# Created: 2021.02.28
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import os
from jinja2 import Environment, FileSystemLoader
#
from Inc.DataClass import DDataClass
from Inc.Misc.Request import TRequestJson, TAuth
from IncP.Plugins import TViewes
from IncP.ApiBase import TApiBase, TApiConf


@DDataClass
class TApiViewConf(TApiConf):
    dir_3w: str = 'view'
    dir_tpl: str = 'IncP/view'
    dir_tpl_cache: str = 'cache/tpl'
    dir_root: str = 'Task/SrvView'
    tpl_ext: str = '.tpl'
    def_page: str = 'info'
    theme: str = 'theme1'


class TApi(TApiBase):
    def __init__(self):
        super().__init__()
        self.Viewes: TViewes
        self.TplEnv: Environment

    @staticmethod
    def _LocateFile(aList: list[str], aDir: str = '') -> str:
        for x in aList:
            Path = aDir + x
            if (os.path.exists(Path)):
                return x

    def Init(self, aConf: TApiConf):
        super().Init(aConf)
        aConf.dir_module = 'IncP/view'
        self.Viewes = TViewes(self.Conf.dir_module)

        Loader = FileSystemLoader(
            searchpath = [
                f'{self.Conf.dir_module}/default/tpl',
                f'{self.Conf.dir_module}/{self.Conf.theme}/tpl'
            ]
        )
        self.TplEnv = Environment(loader = Loader)

TEMPLATE_FILE = "template.html"
template = templateEnv.get_template(TEMPLATE_FILE)
outputText = template.render()  # this is where to put args to th

    async def FormCreate(self, aRequest: web.Request, aName: str, aData: dict = None) -> web.Response:
        FileTpl = self._LocateFile(
            [
                f'{self._SrvConf.theme}/tpl/{aName}{self._SrvConf.tpl_ext}',
                f'default/tpl/{aName}{self._SrvConf.tpl_ext}',
            ],
            self._DirTpl + '/')

        if (FileTpl):
            FilePy = f'{self._DirPy}/{aName}'
        else:
            FilePy = f'{self._DirPy}/{self._SrvConf.def_page}'
            FileTpl = f'default/tpl/{self._SrvConf.def_page}'

        Locate = [
            (FilePy, 'TForm'),
            (f'{self._DirPy}/FormBase', 'TFormBase')
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
        Res = TClass(aRequest, FileTpl, aData)
        Res.Parent = self
        return Res

Api = TApi()
