# Created: 2022.10.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
#
from Inc.DbList import TDbList, TDbRec, TDbRecSafe
from Inc.Util.Obj import DeepGet, DeepGetByList, GetClassPath
from Inc.Misc.Time import TASleep
from Inc.Misc.Request import TRequestGet, TRequestJson
from IncP.Log import Log


class TTranslate():
    def __init__(self):
        self.DelMpn = ''.maketrans('', '', ' -/_.&@()#+"')

    def GetMpn(self, aVal) -> str:
        return aVal.translate(self.DelMpn).upper().strip()


class TApiBase():
    def __init__(self):
        self.RequestGet = TRequestGet()
        self.RequestJson = TRequestJson()

    @staticmethod
    def GetModName(aPath: str) -> str:
        return os.path.basename(os.path.dirname(aPath))


class TPluginBase():
    def __init__(self):
        # assigned from TPlugins class creator
        self.Parent = None
        self.Depends = None
        self.Name = None
        self.Conf = None
        self.Depth = 0

    def GetDepends(self) -> list[str]:
        return [x for x in self.Depends if (not x.startswith('-'))]

    def GetParam(self, aName: str, aDef = None) -> object:
        return DeepGet(self.Parent.Data, aName, aDef)

    def GetParamDepends(self, aName: str = '') -> dict:
        Res = {}
        for Depend in self.GetDepends():
            Path = f'{Depend}.{aName}' if (aName) else Depend
            Param = self.GetParam(Path)
            if (Param):
                Res[Depend] = Param
        return Res

    def GetParamDependsIdx(self, aName: str, aIdx: int = 0) -> object:
        Param = self.GetParamDepends(aName)
        Param = list(Param.values())
        if (aIdx < len(Param)):
            return Param[aIdx]
        return None

    def GetParamExport(self, aName: str) -> dict:
        Module = self.__module__.rsplit('.', maxsplit = 1)[-1]
        return DeepGetByList(self.Parent.Conf, ['plugin', aName, 'export', Module], {})

    def GetFile(self) -> str:
        Res = self.Conf.GetKey('file')
        if (not Res):
            Split = self.Name.split('_')
            File = '/'.join(Split[:-1]) + '.' + Split[-1]
            Res = self.Parent.Conf.GetKey('dir_data') + '/' + File
        return Res


class TFileBase():
    def __init__(self, aParent):
        self.Parent = aParent
        self.Sleep = TASleep(self.Parent.Conf.get('sleep_loop', 0), 500)

    def GetFile(self) -> str:
        TopClass = GetClassPath(self).split('/')[-1]
        Res = self.Parent.Parent.Conf.GetKey('dir_data') + '/' + self.Parent.Name + '/' + TopClass + '.dat'
        return Res


class TFileDbl(TFileBase):
    def __init__(self, aParent, aDbl: TDbList):
        super().__init__(aParent)
        self.Dbl = aDbl

    async def _Load(self):
        raise NotImplementedError()

    def _OnLoad(self):
        pass

    def Copy(self, aName: str, aRow: dict, aRec: TDbRec):
        Val = aRow.get(aName)
        if (Val is None):
            Val = aRec.Def.get(aName)
        aRec.SetField(aName, Val)

    def CopySafe(self, aName: str, aRow: dict, aRec: TDbRecSafe):
        Field = self.Dbl.Fields[aName]
        Val = aRow.get(aName)
        if (Val is None):
            Val = Field[2]
        elif (not isinstance(Val, Field[1])):
            Val = Field[1](Val)
        aRec.SetField(aName, Val)

    async def Load(self):
        File = self.GetFile()
        Log.Print(1, 'i', f'Load {File}')
        if (os.path.exists(File)):
            self.Dbl.Load(File)
        else:
            ClassPath = GetClassPath(self)
            if (any(x in ClassPath for x in ['_xls', '_xlsx', '_ods', '_csv',  '_xml'])):
                SrcFile = self.Parent.GetFile()
                if (not os.path.exists(SrcFile)):
                    Log.Print(1, 'e', f'File not found {SrcFile}. Skip')
                    return

            self._OnLoad()
            await self._Load()
            if (self.Parent.Conf.get('save_cache')):
                os.makedirs(os.path.dirname(File), exist_ok=True)
                self.Dbl.Save(File, True)
        Log.Print(1, 'i', f'Done {File}. Records {self.Dbl.GetSize()}')


class TEngine(TFileDbl):
    def __init__(self, aParent, aDbl):
        super().__init__(aParent, aDbl)

        self._Engine = None
        self._Sheet = 'default'

    def _InitEngine(self, aFile: str):
        raise NotImplementedError()

    def GetConfSheet(self) -> dict:
        Res = DeepGetByList(self.Parent.Conf, ['sheet', self._Sheet])
        assert(Res), f'sheet not found {self._Sheet}'
        return Res

    def InitEngine(self, aEngine = None):
        if (aEngine):
            self._Engine = aEngine
        else:
            ConfFile = self.Parent.GetFile()
            self._Engine = self._InitEngine(ConfFile)
        return self._Engine

    def SetSheet(self, aName: str = ''):
        self._Sheet = aName
