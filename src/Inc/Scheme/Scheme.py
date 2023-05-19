# Created: 2022.03.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

# https://github.com/pythontoday/scrap_tutorial


import datetime
import json
import random
import re
import sys
from urllib.parse import urlparse
#
from Inc.Util.Obj import DeepGet
from Inc.Misc.Python import TPython
from Inc.Misc.Misc import FilterKey, FilterKeyErr
from .SchemeApi import TSchemeApi, TSchemeApiExt, TSchemeExt
from .Utils import SoupGetParents


class TRes():
    def __init__(self, aScheme):
        self.Scheme = aScheme
        self.Clear()

    def Clear(self):
        self.Data = {}
        self.Err = []

    def Exec(self, aPrefix: str, aPy: TPython):
        self.Clear()

        Obj = getattr(self, aPrefix, None)
        if (Obj is None):
            self.Err.append('No method %s' % aPrefix)
            return

        PrefixData = Obj(self.Scheme)
        if (PrefixData is None):
            self.Err.append('Empty data returned')
            return

        Keys = [
            Key
            for Key in dir(self)
            if (Key.startswith(aPrefix)) and Key != aPrefix
        ]

        for Key in Keys:
            Obj = getattr(self, Key, None)
            Name = Key.replace(aPrefix, '')
            if callable(Obj):
                try:
                    Res = Obj(PrefixData)
                    if (Res is None):
                        self.Add(Name, Res, '(none)')
                    else:
                        self.Add(Name, Res)
                except Exception as E:
                    Err = aPy.ErrMsg(E, sys.exc_info())
                    self.Add(Name, None, Err)

    def Add(self, aKey: str, aVal: object, aErr: str = None):
        self.Data[aKey] = aVal
        if (aErr):
            self.Err.append('%s %s' % (aKey, aErr))


class TApiMacro():
    @staticmethod
    def date() -> str:
        return datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')

    @staticmethod
    def rand(aStart: int, aEnd: int) -> int:
        return random.randint(aStart, aEnd)

    @staticmethod
    def prop(aMod: str, aProp: str, aDef = None) -> object:
        __import__(aMod)
        Mod = sys.modules.get(aMod)
        return getattr(Mod, aProp, aDef)

class TSoupScheme():
    def __init__(self):
        self.Debug = False
        self.Clear()
        self.SchemeExt = TSchemeExt(self)

    def Clear(self):
        self.Err = []
        self.Warn = []
        self.Var = {}

    # Syntax ["$date"], ["$rand", [1, 10]], ["$prop", ["IncP", "__version__"]]
    def ParseMacro(self, aItem: list, aPath: str) -> object:
        Func = getattr(TApiMacro, aItem[0][1:], None)
        if (Func):
            try:
                if (len(aItem) > 1):
                    Res = Func(*aItem[1])
                else:
                    Res = Func()
            except Exception as E:
                Res = aItem
                self.Err.append('%s->%s %s (exception)' % (aPath, aItem[0], E))
        else:
            Res = aItem
            self.Err.append('%s->%s (unknown)' % (aPath, aItem))
        return Res

    def ParsePipe(self, aObj, aItem: list, aPath: str) -> object:
        def CallPipe(aClass: object):
            nonlocal aObj, aItem, aPath

            Obj = getattr(aClass, aItem[0])
            Param = [aObj]
            if (len(aItem) == 2):
                Param += aItem[1]

            try:
                aObj = Obj(*Param)
            except Exception as E:
                self.Err.append('%s->%s %s (exception)' % (aPath, aItem, E))
                aObj = None

        Name = aItem[0]
        if (hasattr(TSchemeApiExt, Name)):
            Obj = getattr(TSchemeApiExt, Name)
            if (len(aItem) == 2):
                Item = Obj(*aItem[1])
            else:
                Item = Obj()
            aObj = self.ParsePipes(aObj, Item, aPath)
        elif (hasattr(TSchemeApi, Name)):
            CallPipe(TSchemeApi)
        elif (hasattr(self.SchemeExt, Name)):
            CallPipe(self.SchemeExt)
        else:
            if (self.Debug) and (Name == 'find'):
                if (hasattr(aObj, 'find_all')) and (len(aItem) == 2):
                    Arr = aObj.find_all(*aItem[1])
                    if (len(Arr) > 1):
                        Parents = SoupGetParents(aObj, Arr, 2)
                        self.Warn.append('%s -> %s (found %s)' % (aPath, aItem[1], len(Arr)))
                        for x in Parents:
                            self.Warn.append(str(x))

            aObj = getattr(aObj, Name, None)
            if (aObj):
                if (len(aItem) == 2):
                    try:
                        aObj = aObj(*aItem[1])
                    except Exception as E:
                        self.Err.append('%s->%s %s (exception)' % (aPath, aItem, E))
                        return
            else:
                self.Err.append('%s->%s (unknown)' % (aPath, aItem))
                return

        if (aObj is None):
            self.Err.append('%s->%s (none)' % (aPath, aItem))
        return aObj

    def ParsePipes(self, aObj, aScheme: list, aPath: str) -> object:
        i = 0
        while (aObj) and (i < len(aScheme)):
            Scheme = aScheme[i]
            if (not isinstance(Scheme, list)):
                self.Err.append('%s->%s (not a list)' % (aPath, Scheme))
                return

            Macro = Scheme[0]
            if (not Macro.startswith('-')):
                aPath += '/' + Scheme[0]
                if (Macro == 'as_if'):
                    R = self.ParsePipes(aObj, Scheme[1].get('cond', []), aPath)
                    Cond = str(R is not None).lower()
                    aObj = self.ParsePipes(aObj, Scheme[1].get(Cond), aPath)
                elif (Macro == 'as_list'):
                    aObj = [self.ParsePipes(aObj, x, aPath) for x in Scheme[1]]
                elif (Macro == 'as_dict'):
                    R = {}
                    for Key, Val in Scheme[1].items():
                        if (not Key.startswith('-') and (Val)):
                            R[Key] = self.ParsePipes(aObj, Val, aPath + '/' + Key)
                            self.Var['$' + Key] =  R[Key]
                    aObj = R
                else:
                    aObj = self.ParsePipe(aObj, Scheme, aPath)
            i += 1
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
                            UrlData = urlparse(Val[0])
                            self.Var['$host'] = '%s://%s' % (UrlData.scheme, UrlData.hostname)
        elif (isinstance(aData, list)):
            if (aData[0].startswith('$')):
                Res = self.ParseMacro(aData, aPath)
            else:
                Res = [self._ParseRecurs(aSoup, Val, aPath) for Val in aData]
        else:
            Res = aData
        return Res

    def Parse(self, aSoup, aData: dict) -> dict:
        self.Clear()
        self.Var['$root'] = aSoup
        Res = self._ParseRecurs(aSoup, aData, '')
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

    def Parse(self, aSoup):
        # pylint: disable-next=no-member
        self.Clear()

        if (aSoup):
            Param = {'aVal': aSoup, 'aApi': TSchemeApi, 'aRes': TRes, 'aPy': self.Python}
            Res = self.Python.Exec(Param)
            Err = FilterKeyErr(Res)
            if (Err):
                self.Err = Res.get('data')
            else:
                Data = Res.get('data')
                self.Data = Data.get('data', {})
                self.Err = Data.get('err', [])

                self.Pipe = FilterKey(self.Data, self.GetFields(), dict)
        return self

    def GetUrl(self) -> list:
        #Match = re.search('Url\s*=\s*(.*?)$', self.Scheme, re.DOTALL)
        Match = re.search(r'(?P<url>http[s]?://[^\s]+)', self.Python.Script, re.DOTALL)
        if (Match):
            return [Match.group('url')]

    def GetFields(self) -> list:
        raise NotImplementedError()


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

    def Parse(self, aSoup):
        # pylint: disable-next=no-member
        self.Clear()
        if (aSoup):
            SoupScheme = TSoupScheme()
            SoupScheme.Debug = self.Debug
            self.Data = SoupScheme.Parse(aSoup, self.Scheme)
            self.Err = SoupScheme.Err
            self.Warn = SoupScheme.Warn

            self.Pipe = FilterKey(self.Data, self.GetFields(), dict)
        return self

    def GetUrl(self) -> list:
        return DeepGet(self.Scheme, 'product.info.url')

    def GetFields(self) -> list:
        raise NotImplementedError()


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
            return self.__class__.__bases__[0] == TSchemeJson

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

        def GetFields(self) -> list:
            return ['image', 'price', 'price_old', 'name', 'stock', 'mpn', 'sku', 'category', 'description']

        def GetPipe(self) -> dict:
            return {Key.split('.')[-1]: Val for Key, Val in self.Pipe.items()}

    return TClass(aScheme)
