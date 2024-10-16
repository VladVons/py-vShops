# Created: 2022.10.10
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import re
import json
#
from .Misc import TJsonEncoder


def DirWalk(aPath: str, aMask: str = '.*', aType: str = 'f', aDepthMax: int = 99) -> iter:
    '''
    aMask - regExp mask
    aType: f - file, d - directory
    aDepthMax: max recursion depth
    for (Path, Type, aDepth) in DirWalk('/etc', '.jpg$|.png$', 'fd', 5)
    '''

    def Recurs(aPath: str, aDepth: int) -> iter:
        for File in sorted(os.listdir(aPath)):
            Path = aPath + '/' + File

            Type = 'd' if (os.path.isdir(Path)) else 'f'
            if (Type == 'd') and (aDepth < aDepthMax) and (not os.path.islink(Path)):
                yield from Recurs(Path, aDepth + 1)

            if (Type in aType) and ((aMask == '.*') or (re.search(aMask, File))):
                yield (Path, Type, aDepth)
    yield from Recurs(aPath, 0)


def DirRemove(aPath: str) -> list[str]:
    def Recurs(aPath):
        ResFiles = []
        for xFile in os.scandir(aPath):
            if (os.path.isdir(xFile)):
                ResFiles += Recurs(xFile)
                os.rmdir(xFile)
            else:
                os.remove(xFile.path)
                ResFiles.append(xFile.path)
        return ResFiles
    Res = Recurs(aPath)
    os.rmdir(aPath)
    return Res


def FilesExist(aFiles: list[str]) -> list[int]:
    return [int(os.path.exists(File)) for File in aFiles]


def WriteFileTyped(aFile: str, aData):
    if (isinstance(aData, str)):
        with open(aFile, 'w', encoding='utf8') as F:
            F.write(aData)
    if (isinstance(aData, (list, dict, set))):
        with open(aFile, 'w', encoding='utf8') as F:
            json.dump(aData, F, indent=2, ensure_ascii=False, cls=TJsonEncoder)
    else:
        with open(aFile, 'wb') as F:
            F.write(aData)
