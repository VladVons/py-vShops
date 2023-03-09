# Created: 2022.03.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import sys


def GetImportsLocal() -> set[str]: #//
    Res = set()
    for _Name, Val in globals().items():
        Type = type(Val).__name__
        if (Type == 'module'):
            Res.add(Val.__name__)
        elif (Type == 'type'):
            ModName = sys.modules[Val.__module__].__name__
            Res.add(ModName.split('.')[0])
    return Res

def GetImportsGlobal() -> set[str]: #//
    Res = set()
    for Name in sys.modules:
        if (not Name.startswith('_')):
            Res.add(Name.split('.')[0])
    return Res

def DynImport(aPath: str, aClass: str) -> object: #//
    try:
        Mod = __import__(aPath, None, None, [aClass])
        TClass = getattr(Mod, aClass, None)
    except ModuleNotFoundError as E:
        print(E)
    else:
        return TClass

#---
#http://www.qtrac.eu/pyclassmulti.html

def DAddMethods(aMethods: list):
    def Decor(aClass):
        for Method in aMethods:
            setattr(aClass, Method.__name__, Method)
        return aClass
    return Decor

def DAddModules(aModules: list, aSeparate: bool = False):
    def Decor(aClass):
        for Module in aModules:
            if (aSeparate):
                Name = Module.__name__.split('.')[-1]
                setattr(aClass, Name, Module)
            else:
                for Method in dir(Module):
                    if (not Method.endswith('__')):
                        Obj = getattr(Module, Method)
                        setattr(aClass, Method, Obj)
        return aClass
    return Decor

#---
