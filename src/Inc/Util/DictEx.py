# Created: 2024.09.23
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
import os
import sys
import json
#
from Inc.Misc.IniFile import TIniFile
from . Dict import DeepGet


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
                if (Type == 'env'):
                    aVal = os.getenv(Val)
                    assert(aVal), f'Unknown environment variable {Val}'
                elif (Type == 'file_json'):
                    File, Key = GetFileMacros(Val)

                    with open(File, 'r', encoding = 'utf8') as F:
                        aVal = json.load(F)

                    if (Key):
                        aVal = DeepGet(aVal, Key[0])
                elif (Type == 'file_ini'):
                    File, Key = GetFileMacros(Val)

                    Ini = TIniFile()
                    Ini.Read(File)
                    if (Key):
                        Sect = Key[0]
                        assert(Sect in Ini.GetSections()), f'Section {Sect} not found'
                        aVal = Ini.GetData(Sect)
                    else:
                        aVal = Ini.GetData('')
                elif (Type == 'arg'):
                    if (Val in sys.argv):
                        Idx = sys.argv.index(Val)
                        aVal = sys.argv[Idx + 1]
                else:
                    raise ValueError(f'Macros {Type}')
        return aVal

    if (aDepth <= 0):
        return

    Type = type(aSlave)
    if (Type == dict):
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
    elif (Type == list):
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

# more complex https://jmespath.org/examples.html
# Data = {'table': {'ref_product': {'foreign_key': {'tenant_id': {'table': 'x'}}}}}
# DeepGetRe(Data, ['^table', '.*_lang', '.*', '.*_id$', '.*'])
def DeepGetsRe(aObj, aKeys: list, aWithPath: bool = True) -> list:
    RegExSign = '.*+^$[({'

    def Recurs(aObj, aKeys: list, aPath: str) -> list:
        Res = []
        if (aKeys):
            Type = type(aObj)
            if (Type == dict):
                Key = aKeys[0]
                if (any(x in RegExSign for x in Key)):
                    for xKey in aObj:
                        if (re.match(Key, xKey)):
                            Res += Recurs(aObj.get(xKey), aKeys[1:], f'{aPath}.{xKey}')
                else:
                    Val = aObj.get(Key)
                    if (Val is not None):
                        Res += Recurs(Val, aKeys[1:], f'{aPath}.{Key}')
            elif (Type in [list, tuple, set]):
                for Idx, Val in enumerate(aObj):
                    Res += Recurs(Val, aKeys, f'{aPath}[{Idx}]')
        else:
            if (aWithPath):
                Res.append((aObj, aPath.lstrip('.')))
            else:
                Res.append(aObj)
        return Res
    return Recurs(aObj, aKeys, '')
