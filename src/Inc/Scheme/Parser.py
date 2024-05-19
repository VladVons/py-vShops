# Created: 2022.03.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import sys
import datetime
import random
#
from Inc.Misc.Python import TPython


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

class TSchemeBase():
    def __init__(self):
        self.Debug = False
        self.RegEmpty = True
        self.Clear()

    def Clear(self):
        self.Err = []
        self.Warn = []
        self.Var = {}

    def _CallPipe(self, aObj, aItem: list, aPath: str, aClass: object) -> object:
        Obj = getattr(aClass, aItem[0])
        Param = [aObj]
        if (len(aItem) == 2):
            Param += aItem[1]

        try:
            aObj = Obj(*Param)
        except Exception as E:
            self.Err.append('%s->%s %s (exception)' % (aPath, aItem, E))
            aObj = None
        return aObj

    def _ParsePipeDef(self, aObj, aItem: list, aPath: str) -> object:
        aObj = getattr(aObj, aItem[0], None)
        if (aObj):
            ParamCnt = len(aItem)
            if (ParamCnt >= 2):
                try:
                    Param1 = aItem[1]
                    if (ParamCnt == 2):
                        aObj = aObj(*Param1)
                    elif (ParamCnt == 3):
                        if (Param1):
                            aObj = aObj(*Param1, **aItem[2])
                        else:
                            aObj = aObj(**aItem[2])
                except Exception as E:
                    self.Err.append('%s->%s %s (exception)' % (aPath, aItem, E))
                    return
        else:
            self.Err.append('%s->%s (unknown)' % (aPath, aItem))
            aObj = None
        return aObj

    def ParsePipe(self, aObj, aItem: list, aPath: str) -> object:
        raise NotImplementedError()

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
                            Res = self.ParsePipes(aObj, Val, aPath + '/' + Key)
                            if (Res or self.RegEmpty):
                                R[Key] = Res
                                self.Var['$' + Key] =  R[Key]
                    aObj = R
                else:
                    aObj = self.ParsePipe(aObj, Scheme, aPath)
            i += 1
        return aObj
