# Created: 2022.03.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import sys
import re


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

def DynImport(aPath: str, aClass: str) -> tuple:
    TClass, Err = (None, None)
    try:
        Mod = __import__(aPath, None, None, [aClass])
        TClass = getattr(Mod, aClass, None)
        if (not TClass):
            Err = f'Class {aClass} not found in {aPath}'
    except ModuleNotFoundError as E:
        Err = str(E)
    return (TClass, Err)

#---
#http://www.qtrac.eu/pyclassmulti.html


def _AddModules(aClassA: object, aModules: list, aAs: str = None):
    def FilterDunder(aClassB: object, aModule: object):
        for Method in dir(aModule):
            if (not Method.endswith('__')):
                Obj = getattr(Module, Method)
                setattr(aClassB, Method, Obj)

    for Module in aModules:
        if (aAs):
            if (aAs == '*'):
                Name = Module.__name__.split('.')[-1]
                setattr(aClassA, Name, Module)
            else:
                Class = getattr(aClassA, aAs, None)
                if (not Class):
                    Class = type('TClass', (object,), {})
                FilterDunder(Class, Module)
                setattr(aClassA, aAs, Class)
        else:
            FilterDunder(aClassA, Module)

def DAddMethods(aMethods: list):
    def Decor(aClass):
        for Method in aMethods:
            setattr(aClass, Method.__name__, Method)
        return aClass
    return Decor

def DAddModules(aModules: list, aAs: str = None):
    def Decor(aClass):
        _AddModules(aClass, aModules, aAs)
        return aClass
    return Decor

def DAddFiles(aPath: str, aMask: str, aAs: str = None):
    '''
    Add modules to class. aAs can be one of <None, *, Name>
    @DAddFiles(__name__, 'Api.*', 'MyApi')
    class TMyClass(): pass
    '''
    def Decor(aClass):
        Modules = []
        Path = aPath.replace('.', '/')
        for File in os.listdir(Path):
            if (re.search(aMask, File)):
                PathMod = '%s.%s' % (aPath, File.rsplit('.', maxsplit = 1)[0])
                __import__(PathMod)
                Module = sys.modules.get(PathMod)
                Modules.append(Module)
        _AddModules(aClass, Modules, aAs)
        return aClass
    return Decor

#---
