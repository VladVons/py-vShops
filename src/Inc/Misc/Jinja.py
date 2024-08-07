import os
import re
from jinja2 import Environment, BaseLoader, Template
from jinja2.exceptions import TemplateNotFound
#
from Inc.DbList import TDbList
from Inc.Util.Obj import GetTree


def Text2Html(aText: str) -> str:
    if (aText):
        #aText = aText.replace('\n-', '\n<li>')
        aText = aText.replace('\n', '<br>')
    return aText

def Dump(self, aDepth = 0, aName: str = '') -> str:
    '''
    in template use {{Dump(self, 2, 'lang/')}}
    '''
    Res = []
    #pylint: disable-next=protected-access
    Vars = self._TemplateReference__context.parent
    for Key, Val in Vars.items():
        if (isinstance(Val, (str, int, float, dict, list))):
            for (Nested, Path, Obj, _Depth) in GetTree(Val, aDepth + 1):
                Name = f'{Key}{Path}'
                if (aName == '' or Name.startswith(aName)) and (not 'method' in Key) and (not 'method' in Name):
                    Data = f'{Name} ({type(Obj).__name__})'
                    if (not Nested):
                        Data += f' = {Obj}'
                    print(Data)
                    Res.append(Data)
    return '<br>\n'.join(Res)

def Type(aVar) -> str:
    return f'{aVar} {type(aVar).__name__}'

class TFileSystemLoader(BaseLoader):
    def __init__(self, aSearchPath: list[str] = None):
        self.SearchPath = aSearchPath or []
        for x in self.SearchPath:
            assert(os.path.isdir(x)), f'Directory not exists {x}'

    def SearchFile(self, aFile: str) -> str:
        if (self.SearchPath):
            for Path in self.SearchPath:
                File = f'{Path}/{aFile}'
                if (os.path.isfile(File)):
                    return File
        elif (os.path.isfile(aFile)):
            return aFile

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
        Dir = parent.rsplit('/', maxsplit = 1)[0]
        if (template.startswith('./')):
            template = f'{Dir}{template[1:]}'
        elif (template.startswith('../')):
            template = f'{Dir}/{template}'
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
        self.Env.globals['Dump'] = Dump
        self.Env.globals['Text2Html'] = Text2Html
        self.Env.globals['Type'] = Type
        #self.Env.filters['MyFunc'] = MyFunc
        self.Env.trim_blocks = True
        self.Env.lstrip_blocks = True

        #self.ReVar = re.compile(r'''[{]{1,2}%?\s*([a-z-_]+)\s*['"]?([^'"}]*)['"]*\s*%?[}]{1,2}''')
        self.ReMacro = re.compile(r'''\{%\s*(\w+)\s*['"]?([\w/.]+)['"]?\s*%\}''')
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
