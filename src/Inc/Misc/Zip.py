# Created: 2022.10.27
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import io
import zipfile


def PackDictToStream(aData: dict) -> io.BytesIO:
    Res = io.BytesIO()
    with zipfile.ZipFile(Res, mode = 'w', compression=zipfile.ZIP_DEFLATED) as ZF:
        for Key, Val in aData.items():
            ZF.writestr(Key, Val)
    return Res

def PackFilesToStream(aFiles: list[str]) -> io.BytesIO:
    Files = {}
    for File in aFiles:
        if (File):
            if (os.path.exists(File)):
                Name = os.path.basename(File)
                with open(File, 'r', encoding='utf-8') as F:
                    Files[Name] = F.read()
            else:
                #Log.Print(1, 'e', f'ZipFilesToStream(). File not found {File}')
                pass
    return PackDictToStream(Files)

def PackFiles(aFileOut: str, aFiles: list[str], aWithPath: bool = True):
    with zipfile.ZipFile(aFileOut, mode = 'w', compression=zipfile.ZIP_DEFLATED) as ZF:
        for File in aFiles:
            if (aWithPath):
                ZF.write(File)
            else:
                ZF.write(File, os.path.basename(File))

def Extract(aFile: str, aDir: str):
    with zipfile.ZipFile(aFile, 'r') as F:
        F.extractall(aDir)
