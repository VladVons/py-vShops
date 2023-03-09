# Created:     2022.10.22
# Author:      Vladimir Vons <VladVons@gmail.com>
# License:     GNU, see LICENSE for more details


'''
from Inc.DataClass import DDataClass, is_dataclass

@DDataClass
class TUser():
    Login: str
    Passw: str
    Allow: bool = True

@DDataClass(aFrozen = True)
class TUserInherit(TUser):
    Age: int

User = TUser(Login = 'MyLogin', Passw = 'MyPassw')
print('str', str(User))
print('is_dataclass', is_dataclass(User))

UserInherit = TUserInherit(Login = 'MyLogin', Passw = 'MyPassw', Age = 33)
print('Age', UserInherit.Age)

## Error is OK. Frozen class
UserInherit.Age = 34
'''


import sys
import builtins


__all__ = ['DDataClass', 'asdict', 'astuple', 'is_dataclass', 'get_def', 'set_safe']

_Type = '_type_'
_Dflt = '_dflt_'
_Cnf = '_cnf_'

def get_def(aCls, aName: str, aDef = None) -> object:
    if (hasattr(aCls, aName)):
        return getattr(aCls, aName)
    return aDef

def set_safe(aCls, aDict: dict):
    for Key, Val in aDict.items():
        if (hasattr(aCls, Key)):
            setattr(aCls, Key, Val)

def is_dataclass(aCls) -> bool:
    return hasattr(aCls, _Cnf)

def asdict(aCls) -> dict:
    return aCls.__dict__

def astuple(aCls) -> dict:
    return [(Key, Val) for Key, Val in aCls.__dict__.items()]

def _Repr(aCls) -> str:
    Human = [f'{Key}={Val}' for Key, Val in aCls.__dict__.items()]
    return aCls.__class__.__name__ + '(' + ', '.join(Human) + ')'

def _SetAttr(aCls, aKey, aVal):
    raise ValueError(f'Class {aCls.__class__.__name__} is frozen')

def _GetArgs(aCls, aData: dict) -> str:
    Args = []
    for Name, Type in aData.items():
        if (Type.__module__ == 'builtins'):
            Param = f'{Name}: {Type.__name__}'
        else:
            Param = f'{Name}: {_Type}{Name}'

        HasDefVal = hasattr(aCls, Name)
        if (HasDefVal):
            Param += f' = {_Dflt}{Name}'
        Args.append(Param)
    return 'self, ' + ', '.join(Args)

def _Compile(aCls, aName: str, aData: dict) -> object:
    Globals = {}
    if (aCls.__module__ in sys.modules):
        Globals = sys.modules[aCls.__module__].__dict__

    BuiltIns = '_BltIn_'
    Locals = {}
    Locals[BuiltIns] = builtins

    Cnf = getattr(aCls, _Cnf)
    CnfFrozen = Cnf['frozen']

    Body = []
    Args = _GetArgs(aCls, aData)
    Body.append(f' def {aName}({Args}):')
    for Name, Type in aData.items():
        NameK = f'{_Type}{Name}'
        Locals[NameK] = Type

        HasDefVal = hasattr(aCls, Name)
        if (HasDefVal):
            Default = getattr(aCls, Name)
            NameK =f'{_Dflt}{Name}'
            Locals[NameK] = Default

        if (CnfFrozen):
            Body.append(f'  {BuiltIns}.object.__setattr__(self, "{Name}", {Name})')
        else:
            Body.append(f'  self.{Name} = {Name}')
    Body.append(f' return {aName}')

    Wrapper = '__create_fn__'
    LocalsVar = ', '.join(Locals.keys())
    Body.insert(0, f'def {Wrapper}({LocalsVar}):')
    Body = '\n'.join(Body)

    Out = {}
    # pylint: disable-next=exec-used
    exec(Body, Globals, Out)
    Res = Out[Wrapper](**Locals)
    return Res

def _GetAnnotations(aCls) -> dict:
    Res = {}
    for x in aCls.__mro__:
        Data = x.__dict__.get('__annotations__')
        if (Data):
            Res.update(Data)
    return Res

def _ProcessClass(aCls, aFrozen: bool, aRepr: bool) -> object:
    Cnf = {'frozen': aFrozen, 'repr': aRepr}
    setattr(aCls, _Cnf, Cnf)

    if (aFrozen):
        aCls.__setattr__ = _SetAttr

    if (aRepr):
        aCls.__repr__ = _Repr

    Name = '__init__'
    Annotations = _GetAnnotations(aCls)
    Data = _Compile(aCls, Name, Annotations)
    Data.__qualname__ = f'{aCls.__class__.__name__}.{Data.__name__}'
    setattr(aCls, Name, Data)
    return aCls

# Decorator
def DDataClass(aCls = None, aFrozen: bool = False, aRepr: bool = True) -> object:
    def Wrap(aCls):
        return _ProcessClass(aCls, aFrozen, aRepr)

    # as @DDataClass()
    if (aCls is None):
        return Wrap

    # as @DDataClass
    return Wrap(aCls)
