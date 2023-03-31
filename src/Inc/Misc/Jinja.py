import os
import re
from jinja2 import Environment, BaseLoader, Template
from jinja2.exceptions import TemplateNotFound
#
from Inc.DbList import TDbList


class TFileSystemLoader(BaseLoader):
    def __init__(self, aSearchPath: list[str]):
        self.SearchPath = aSearchPath

    def SearchFile(self, aFile: str) -> str:
        for Path in self.SearchPath:
            File = f'{Path}/{aFile}'
            if (os.path.isfile(File)):
                return File

    def LoadFile(self, aFile: str) -> str:
        with open(aFile, 'r', encoding = 'utf-8') as F:
            return F.read()

    def get_source(self, environment: Environment, template: str) -> tuple:
        File = self.SearchFile(template)
        if (not File):
            raise TemplateNotFound(template)

        Data = self.LoadFile(File)
        MTime = os.path.getmtime(File)
        return (Data, File, lambda: MTime == os.path.getmtime(File))

    def list_templates(self) -> list[str]:
        raise NotImplementedError()


class TEnvironment(Environment):
    TplCache = {}

    def FromFile(self, aSource, aName: str, aFile: str) -> Template:
        Res = self.TplCache.get(aName)
        if (not Res):
            gs = self.make_globals(None)
            cls = self.template_class
            Res = cls.from_code(self, self.compile(aSource, aName, aFile), gs, None)
            self.TplCache[aName] = Res
        return Res

    def join_path(self, template: str, parent: str) -> str:
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


class TTemplate():
    def __init__(self, aPaths: list[str]):
        self.Ext = 'j2'
        Loader = TFileSystemLoader(aPaths)

        self.Env = TEnvironment(loader = Loader)
        self.Env.globals['TDbList'] = TDbList
        self.Env.trim_blocks = True
        self.Env.lstrip_blocks = True
        #self.Env.filters['MyFunc'] = MyFunc

        #self.ReVar = re.compile(r'''[{]{1,2}%?\s*([a-z-_]+)\s*['"]?([^'"}]*)['"]*\s*%?[}]{1,2}''')
        self.ReVar = re.compile(r'\{\{\s*(\w+)\s*\}\}')

    def SearchFile(self, aFile: str) -> str:
        return self.Env.loader.SearchFile(aFile)

    def SearchModule(self, aPath: str) -> str:
        return self.SearchFile(f'{aPath}.{self.Ext}')

    def RenderInc(self, aFile: str, aData: dict) -> str:
        Source, File, _ = self.Env.loader.get_source(self.Env, aFile)
        Vars = self.ReVar.findall(Source)
        for x in Vars:
            if (x.startswith('inc_')):
                File = '%s/%s.%s' % (aFile.rsplit('/', maxsplit = 1)[0], x, self.Ext)
                aData[x] = self.RenderInc(File, aData.get(x, {}))
        Tpl = self.Env.FromFile(Source, aFile, File)
        return Tpl.render(aData)

    def Render(self, aFile: str, aData: dict) -> str:
        Tpl = self.Env.get_template(aFile)
        return Tpl.render(aData)
