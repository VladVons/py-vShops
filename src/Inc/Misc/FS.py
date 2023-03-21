# Created: 2022.10.10
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import re


def DirWalk(aPath: str, aMask: str = '.*', aType: str = 'f', aDepthMax: int = 99) -> iter:
    '''
    aMask - regExp mask
    aType: f - file, d - directory
    aDepthMax: max recursion depth
    for (Path, Type, aDepth) in DirWalk('/etc', '.bin$', 'fd', 5)
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


def DirRemove(aPath: str):
    for File in os.scandir(aPath):
        if (os.path.isdir(File)):
            DirRemove(File)
            os.rmdir(File)
        else:
            os.remove(File.path)

def FilesExist(aFiles: list[str]) -> list[int]:
    return [int(os.path.exists(File)) for File in aFiles]
