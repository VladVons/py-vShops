# Created: 2024.09.23
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
import os
import sys
import json
#
from Inc.Misc.IniFile import TIniFile
from .Dict import DeepGet


def DictUpdateDeep(aMaster: dict, aSlave: dict, aJoin = False, aDepth: int = 99) -> object:
    '''
    DictJoin({3: [1, 2, 3]}, {3: [4]}) -> {3: [1, 2, 3, 4]}
    '''

    def GetFileMacros(aMacro: str) -> tuple:
        File, *Key = aMacro.rsplit(':', maxsplit=1)
        File = os.path.expanduser(File)
        return (File, Key)

    def ParseEnv(aVal) -> object:
        if (isinstance(aVal, str)) and (aVal.startswith('{%')):
            Macro = re.findall(r'''\{%\s*(\w+)\s*([\w/.:-~]+)\s*%\}''', aVal)
            if (Macro):
                Type, Val = Macro[0]
                match Type:
                    case 'env':
                        aVal = os.getenv(Val)
                        assert(aVal), f'Unknown environment variable {Val}'
                    case 'file_json':
                        File, Key = GetFileMacros(Val)

                        with open(File, 'r', encoding = 'utf8') as F:
                            aVal = json.load(F)

                        if (Key):
                            aVal = DeepGet(aVal, Key[0])
                    case 'file_ini':
                        File, Key = GetFileMacros(Val)

                        Ini = TIniFile()
                        Ini.Read(File)
                        if (Key):
                            Sect = Key[0]
                            assert(Sect in Ini.GetSections()), f'Section {Sect} not found'
                            aVal = Ini.GetData(Sect)
                        else:
                            aVal = Ini.GetData('')
                    case 'arg':
                        if (Val in sys.argv):
                            Idx = sys.argv.index(Val)
                            aVal = sys.argv[Idx + 1]
                    case _:
                        raise ValueError(f'Macros {Type}')
        return aVal

    if (aDepth <= 0):
        return

    if isinstance(aSlave, dict):
        if (aMaster is None):
            aMaster = {}
        Res = aMaster

        for Key, Val in aSlave.items():
            Val = ParseEnv(Val)
            Tmp = aMaster.get(Key)
            if (Tmp is None):
                Tmp = {} if isinstance(Val, dict) else []
            Data = DictUpdateDeep(Tmp, Val, aJoin, aDepth - 1)
            Res[Key] = Data
    elif isinstance(aSlave, list):
        Res = [] if (aMaster is None ) else aMaster
        for Val in aSlave:
            Val = ParseEnv(Val)
            Data = DictUpdateDeep(None, Val, aJoin, aDepth - 1)
            if (aJoin):
                Res.append(Data)
            else:
                Res = Data
    else:
        Res = aSlave
    return Res

# see DictEx.txt. more complex use https://jmespath.org/examples.html
def DeepGetsRe(aObj, aKeys: list, aWithPath: bool = True) -> list:
    RegExSign = '.*+^?$[({'

    def Recurs(aObj, aKeys: list, aPath: str) -> list:
        Res = []
        if (aKeys):
            Key = aKeys[0]
            if (isinstance(aObj, dict)):
                if (not isinstance(Key, str)):
                    return Res

                if (any(x in RegExSign for x in Key)):
                    for xKey in aObj:
                        if (re.search(Key, xKey)):
                            Res += Recurs(aObj.get(xKey), aKeys[1:], f'{aPath}.{xKey}')
                else:
                    Val = aObj.get(Key)
                    if (Val is not None):
                        Res += Recurs(Val, aKeys[1:], f'{aPath}.{Key}')
            elif (isinstance(aObj, (list, tuple, set))):
                Indexes = []
                for xKey in Key:
                    if (isinstance(xKey, int)):
                        Indexes.append(xKey)
                    elif (isinstance(xKey, (list, tuple))):
                        Indexes += range(*slice(*xKey).indices(len(aObj)))

                for Idx, Val in enumerate(aObj):
                    if (not Key) or (Idx in Indexes):
                        Res += Recurs(Val, aKeys[1:], f'{aPath}[{Idx}]')
        else:
            if (aWithPath):
                Res.append((aObj, aPath.lstrip('.')))
            else:
                Res.append(aObj)
        return Res
    return Recurs(aObj, aKeys, '')
