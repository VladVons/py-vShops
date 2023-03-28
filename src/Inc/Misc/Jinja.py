import os
from jinja2 import Environment, BaseLoader, meta
from jinja2.exceptions import TemplateNotFound
#
from Inc.Util.Obj import DeepGetByList
from Inc.DbList import TDbList


class TFileSystemLoader(BaseLoader):
    def __init__(self, aSearchPath: list[str]):
        self.SearchPath = aSearchPath

    def GetFile(self, aFile: str) -> str:
        for Path in self.SearchPath:
            File = f'{Path}/{aFile}'
            if (os.path.isfile(File)):
                return File

    def LoadFile(self, aFile: str) -> str:
        with open(aFile, 'r', encoding = 'utf-8') as F:
            return F.read()

    def get_source(self, environment: Environment, template: str) -> tuple:
        File = self.GetFile(template)
        if (not File):
            raise TemplateNotFound(template)

        Data = self.LoadFile(File)
        MTime = os.path.getmtime(File)
        return (Data, File, lambda: MTime == os.path.getmtime(File))

    def list_templates(self) -> list[str]:
        raise NotImplementedError()


class TEnvironment(Environment):
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
        #self.Env.filters['MyFunc'] = MyFunc

    def GetFile(self, aFile: str) -> str:
        return self.Env.loader.GetFile(aFile)

    def GetModuleFile(self, aPath: str) -> str:
        return self.GetFile(f'{aPath}.{self.Ext}')

    def RenderFile(self, aFile: str, aData: dict) -> str:
        Source = self.Env.loader.LoadFile(aFile)
        Content = self.Env.parse(Source)
        Vars = meta.find_undeclared_variables(Content)
        for x in Vars:
            if (x.startswith('inc_')):
                File = '%s/%s.j2' % (aFile.rsplit('/', maxsplit = 1)[0], x)
                Name = x.replace('inc_', '')
                Data = DeepGetByList(aData, ['ctrl', 'modules', Name], {})
                aData[x] = self.RenderFile(File, Data)

        Tpl = self.Env.from_string(Source)
        return Tpl.render(aData)
