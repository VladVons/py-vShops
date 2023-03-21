# Created: 2022.10.10
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import re


def GetFiles(aPath: str, aMask: str = '.*', aType: str = 'f', aDepth: int = 99):
    '''
    iterator function
    aMask - regExp mask
    aType: f - file, d - directory
    aDepth: max recursion depth
    for x in GetFiles('/etc', '.bin$', 'fd')
    '''

    if (os.path.exists(aPath)):
        for File in sorted(os.listdir(aPath)):
            Path = aPath + '/' + File
            Type = 'd' if (os.path.isdir(Path)) and (not os.path.islink(Path)) else 'f'
            if (Type == 'd') and (aDepth >= 0):
                yield from GetFiles(Path, aMask, aType, aDepth - 1)

            if (Type in aType) and (re.search(aMask, File)):
                yield Path

def DirRemove(aPath: str):
    for File in os.scandir(aPath):
        if (os.path.isdir(File)):
            DirRemove(File)
            os.rmdir(File)
        else:
            os.remove(File.path)

def FilesExist(aFiles: list[str]) -> list[int]:
    return [int(os.path.exists(File)) for File in aFiles]
    def Recurs(aPath: str, aDepth: int):
