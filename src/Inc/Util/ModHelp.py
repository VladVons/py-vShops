# Created: 2023.02.22
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
#
from Inc.Util.Types import IsClass, IsFunc, IsFuncA


def GetHelp(aMod: object) -> dict:
    def FindFunc(aName) -> str:
        nonlocal Func
        for x in Func:
            if (x[0].startswith(aName + '(')):
                return x[0]

    def Recurs(aObj, aRes: dict):
        for xDir in dir(aObj):
            if (not xDir.startswith('_')):
                Obj = getattr(aObj, xDir)
                if (IsFunc(Obj) or IsFuncA(Obj)) and (aMod.__name__ == Obj.__module__):
                    if ('func' not in aRes):
                        aRes['func'] = []
                    ResF = GetMethod(Obj)
                    Data = {'name': ResF[0], 'decl': FindFunc(ResF[0]), 'doc': ResF[3]}
                    aRes['func'].append(Data)
                elif IsClass(Obj) and (aMod.__name__ == Obj.__module__):
                    if ('class' not in aRes):
                        aRes['class'] = []
                    Data = {'name': xDir}
                    aRes['class'].append(Data)
                    Recurs(Obj, Data)

    Func = ParseFile(aMod.__file__)
    DocStr = aMod.__doc__ if (aMod.__doc__) else ''
    Res = {'doc': DocStr, 'name': aMod.__name__}
    Recurs(aMod, Res)
    return Res

def ParseFile(aFile: str) -> list: #//
    Res = []
    with open(aFile, 'r', encoding = 'utf-8') as File:
        for x in File.readlines():
            Method = re.findall(r'\s*def\s+(.*?):\s*$', x)
            if (Method):
                Res.append(Method)
    return Res

def GetMethod(aObj) -> list:
    Name = aObj.__code__.co_name
    Args = aObj.__code__.co_varnames[:aObj.__code__.co_argcount]
    Repr = '%s(%s)' % (Name, ', '.join(Args))
    DocString = aObj.__doc__ if (aObj.__doc__) else ''
    return [Name, Args, Repr, DocString]

def GetClass(aClass: object) -> list:
    Res = []
    for x in dir(aClass):
        Obj = getattr(aClass, x)
        if (not x.startswith('_') and hasattr(Obj, '__code__')):
            Res.append(GetMethod(Obj))
    return Res

def GetClassHelp(aModule: object, aClass: object) -> list[str]: #//
    FileInf = ParseFile(aModule.__file__)
    ClassInf = GetClass(aClass)
    for xClassInf in ClassInf:
        Inf = [y[0] for y in FileInf if y[0].startswith(xClassInf[0])]
        if (Inf):
            xClassInf.append(Inf[0])
        else:
            xClassInf.append('')
    return ClassInf

def GetModuleHelp(aModule: object) -> list[str]:
    return GetClassHelp(aModule, aModule)
