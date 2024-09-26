# Created: 2023.02.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#
# fork types.py


import sys
ModuleType = type(sys)

def _Func():
    pass
FunctionType = type(_Func)
CodeType = type(_Func.__code__)

async def _FuncA():
    pass
_Cor = _FuncA()
CoroutineType = type(_Cor)
_Cor.close()

def _Gen():
    yield 1
GeneratorType = type(_Gen())

class _Class:
    def Meth(self):
        pass
ClassType = type(_Class)
MethodType = type(_Class().Meth)

UnionType = type(int or str)
NoneType = type(None)


# ---

def IsFunc(aObj: object) -> bool:
    # magic: __code__
    return isinstance(aObj, FunctionType)

def IsFuncA(aObj: object) -> bool:
    return isinstance(aObj, CoroutineType)

def IsModule(aObj: object) -> bool:
    # magic:__cached__, __doc__, __file__
    return isinstance(aObj, ModuleType)

# def IsClass(aObj: object) -> bool:
#     # magic: __doc__, __module_
#     return isinstance(aObj, type)

def IsClass(aObj: object) -> bool:
    return isinstance(aObj, ClassType)

def IsMethod(aObj: object) -> bool:
    #magic: __doc__,  __name__, __func__,  __self__
    return isinstance(aObj, MethodType)

def IsUnion(aObj: object) -> bool:
    return isinstance(aObj, UnionType)
