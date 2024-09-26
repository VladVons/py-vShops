# Created: 2020.02.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details



def GetTree(aObj, aMaxDepth: int = 99) -> iter:
    '''
        Recursively walks through aObj and returns list of values:
        [Nested, Path, Obj, Depth]
    '''

    def Recurs(aObj, aPrefix: str, aDepth: int):
        if (aDepth < aMaxDepth):
            Type = type(aObj)
            if (Type == dict):
                yield (True, aPrefix, aObj, aDepth)
                for Key in aObj:
                    yield from Recurs(aObj[Key], aPrefix + '/' + Key, aDepth + 1)
            elif (Type in (list, tuple, set)):
                yield (True, aPrefix, aObj, aDepth)
                for Obj in aObj:
                    yield from Recurs(Obj, aPrefix, aDepth + 1)
            elif (Type in (str, int, float, bool)):
                yield (False, aPrefix, aObj, aDepth)
            elif (Type.__name__ in ['method', 'function']):
                yield (False, f'{aPrefix}()', aObj, aDepth)
            else:
                ClassName = aPrefix + '/' + aObj.__class__.__name__
                # if (Types.IsClass(aObj)):
                #     ClassName += '()'
                yield (True, ClassName, aObj, aDepth)
                for Key in dir(aObj):
                    if (not Key.startswith('_')):
                        Obj = getattr(aObj, Key)
                        yield from Recurs(Obj, ClassName + '/' + Key, aDepth + 1)
    yield from Recurs(aObj, '', 0)

def GetClassVars(aClass) -> dict:
    return {
        Key: Val
        for Key, Val in vars(aClass).items()
        if (not callable(Val)) and (not Key.startswith('__'))
    }

def GetClassPath(aClass):
    def GetClassPathRecurs(aInstance: object, aPath: str = '', aDepth: int = 99) -> str:
        Instance = aInstance.__bases__
        if ( (Instance) and (aDepth > 0) ):
            aPath = GetClassPathRecurs(Instance[0], aPath, aDepth - 1)
        return aPath + '/' + aInstance.__name__

    return GetClassPathRecurs(aClass.__class__)

def Iif(aCond: bool, aVal1, aVal2) -> object:
    return aVal1 if (aCond) else aVal2

def IifNone(aVal, aDef) -> object:
    return aDef if (aVal is None) else aVal

def IsDigits(aList: list) -> bool:
    return all(str(x).isdigit() for x in aList)
