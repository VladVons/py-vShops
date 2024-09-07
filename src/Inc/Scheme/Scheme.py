# Created: 2022.03.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

# https://github.com/pythontoday/scrap_tutorial


import json
import re
from urllib.parse import urlparse
#
from Inc.Util.Obj import DeepGetByList
from Inc.Misc.Misc import FilterKeyErr
from Inc.Misc.Python import TPython
from .Parser import TSchemeBase, TRes
from .SchemeApi import TSchemeApi
from .Utils import SoupGetParents
from .SchemeApi import TSchemeApiExt, TSchemeExt


class TSoupScheme(TSchemeBase):
    def __init__(self):
        super().__init__()
        self.SchemeExt = TSchemeExt(self)

    def ParsePipe(self, aObj, aItem: list, aPath: str) -> object:
        Name = aItem[0]
        if (hasattr(TSchemeApiExt, Name)):
            Obj = getattr(TSchemeApiExt, Name)
            if (len(aItem) == 2):
                Item = Obj(*aItem[1])
            else:
                Item = Obj()
            aObj = self.ParsePipes(aObj, Item, aPath)
        elif (hasattr(TSchemeApi, Name)):
            aObj = self._CallPipe(aObj, aItem, aPath, TSchemeApi)
        elif (hasattr(self.SchemeExt, Name)):
            aObj = self._CallPipe(aObj, aItem, aPath, self.SchemeExt)
        else:
            if (self.Debug) and (Name == 'find'):
                if (hasattr(aObj, 'find_all')) and (len(aItem) == 2):
                    Arr = aObj.find_all(*aItem[1])
                    if (len(Arr) > 1):
                        Parents = SoupGetParents(aObj, Arr, 2)
                        self.Warn.append('%s -> %s (found %s)' % (aPath, aItem[1], len(Arr)))
                        for x in Parents:
                            self.Warn.append(str(x))
            aObj = self._ParsePipeDef(aObj, aItem, aPath)

        if (aObj is None):
            self.Err.append('%s->%s (none)' % (aPath, aItem))
        return aObj

    def _ParseRecurs(self, aSoup, aData: dict, aPath: str) -> dict:
        if (isinstance(aData, dict)):
            Res = {}
            for Key, Val in aData.items():
                if (not Key.startswith('-')):
                    Path = aPath + '/' + Key
                    if (Key.startswith('$')):
                        self.Var[Key] = self.ParsePipes(aSoup, Val, Path)
                    elif Key.startswith('pipe'):
                        Res[Key] = self.ParsePipes(aSoup, Val, Path)
                    else:
                        Res[Key] = self._ParseRecurs(aSoup, Val, Path)
                        if (Key == 'url'):
                            UrlData = urlparse(Val[0].lstrip('-'))
                            self.Var['$host'] = '%s://%s' % (UrlData.scheme, UrlData.hostname)
        elif (isinstance(aData, list)):
            if (aData[0].startswith('$')):
                Res = self.ParseMacro(aData, aPath)
            else:
                Res = [self._ParseRecurs(aSoup, Val, aPath) for Val in aData]
        else:
            Res = aData
        return Res

    def Parse(self, aObj: object, aData: dict) -> dict:
        self.Clear()
        self.Var['$root'] = aObj
        Res = self._ParseRecurs(aObj, aData, '')
        return Res


class TSchemePy():
    def __init__(self, aScheme: str):
        self.Err = None
        self.Data = None
        self.Pipe = None

        self.Python = TPython(aScheme)
        self.Python.Compile()
        # pylint: disable-next=no-member
        self.Clear()

    def Parse(self, aObj: object):
        # pylint: disable-next=no-member
        self.Clear()

        if (aObj):
            Param = {'aVal': aObj, 'aApi': TSchemeApi, 'aRes': TRes, 'aPy': self.Python}
            Res = self.Python.Exec(Param)
            Err = FilterKeyErr(Res)
            if (Err):
                self.Err = Res.get('data')
            else:
                Data = Res.get('data')
                self.Data = Data.get('data', {})
                self.Err = Data.get('err', [])
        return self

    def GetUrl(self) -> list:
        #Match = re.search('Url\s*=\s*(.*?)$', self.Scheme, re.DOTALL)
        Match = re.search(r'(?P<url>http[s]?://[^\s]+)', self.Python.Script, re.DOTALL)
        if (Match):
            return [Match.group('url')]


class TSchemeJson():
    def __init__(self, aScheme: dict):
        self.Err = None
        self.Data = None
        self.Pipe = None
        self.Warn = None

        self.Debug = False
        self.Scheme = aScheme
        # pylint: disable-next=no-member
        self.Clear()

    def Parse(self, aObj: object):
        # pylint: disable-next=no-member
        self.Clear()
        if (aObj):
            SoupScheme = TSoupScheme()
            SoupScheme.Debug = self.Debug
            self.Data = SoupScheme.Parse(aObj, self.Scheme)
            self.Err = SoupScheme.Err
            self.Warn = SoupScheme.Warn
        return self

    def GetUrl(self) -> list:
        return DeepGetByList(self.Scheme, ['product', 'info', 'url'])


def TScheme(aScheme: str | dict):
    if (isinstance(aScheme, str)):
        if ('aApi.' in aScheme):
            Class = TSchemePy
        else:
            aScheme = json.loads(aScheme)
            Class = TSchemeJson
    else:
        Class = TSchemeJson

    class TClass(Class):
        def IsJson(self) -> bool:
            #Name = self.__class__.__bases__[0].__name__
            return (self.__class__.__bases__[0] == TSchemeJson)

        def Clear(self):
            self.Data = {}
            self.Pipe = {}
            self.Err = []
            self.Warn = []

        def GetData(self, aKeys: list = None) -> dict:
            if (aKeys is None):
                aKeys = []

            Res = {'data': self.Data, 'err': self.Err, 'pipe': self.Pipe, 'warn': self.Warn}
            if (aKeys):
                Res = {Key: Res.get(Key) for Key in aKeys}
            return Res

        def GetPipe(self, aRoot: str = 'product') -> dict:
            Res = {}
            for xKey1, xVal1 in self.Data[aRoot].items():
                if (isinstance(xVal1, dict) and xKey1.startswith('pipe')):
                    for xKey2, xVal2 in xVal1.items():
                        if (Res.get(xKey2) is None):
                            Res[xKey2] = xVal2
            return Res

    return TClass(aScheme)
