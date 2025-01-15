# Created: 2024.12.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import os
from .Common import TFsBase


class TFsDisk(TFsBase):
    def __init__(self, aRoot: str):
        self.Root = aRoot.replace('/', os.sep)

    @staticmethod
    def _CopyFile(aSrc: str, aDst: str, aChankSize = 1_000_000) -> int:
        Res = 0
        with open(aSrc, 'rb') as FSrc, open(aDst, 'wb') as FDst:
            while Chunk := FSrc.read(aChankSize):
                FDst.write(Chunk)
                Res += len(Chunk)
        return Res

    def _FullPath(self, aPath: str) -> str:
        return f'{self.Root}{os.sep}{aPath.replace('/', os.sep)}'

    def _FullPathCreate(self, aPath: str) -> str:
        Res = aPath.rsplit(os.sep, maxsplit=1)[0] if (os.sep in aPath) else ''
        self.DirCreate(Res)
        return Res

    def Copy(self, aSrc: str, aDst: str) -> bool:
        '''
        copy file or directory from aSrc to aDst.
        '''
        def WCopy(aSrc: str, aDst: str):
            os.makedirs(aDst, exist_ok=True)
            for xFile in os.listdir(aSrc):
                SrcPath = os.path.join(aSrc, xFile)
                DstPath = os.path.join(aDst, xFile)
                if (os.path.isdir(SrcPath)):
                    WCopy(SrcPath, DstPath)
                else:
                    self._CopyFile(SrcPath, DstPath)

        SrcPath = self._FullPath(aSrc)
        if (os.path.exists(SrcPath)):
            DstPath = self._FullPath(aDst)
            if (os.path.isdir(SrcPath)):
                WCopy(SrcPath, DstPath)
            else:
                self._CopyFile(SrcPath, DstPath)
            return True

    def Delete(self, aName: str) -> bool:
        '''
        delete file or directory.
        '''
        def WDirDelete(aPath: str):
            for xFile in os.listdir(aPath):
                File = os.path.join(aPath, xFile)
                if (os.path.isdir(File)):
                    WDirDelete(File)
                else:
                    os.remove(File)
            os.rmdir(File)

        Path = self._FullPath(aName)
        if (os.path.isdir(Path)):
            WDirDelete(Path)
        elif (os.path.isfile(Path)):
            os.remove(Path)
        return not os.path.exists(Path)

    def DirCreate(self, aName: str) -> bool:
        '''
        create directory.
        '''
        Path = self._FullPath(aName)
        if (not os.path.exists(Path)):
            os.makedirs(Path, exist_ok=False)
        return os.path.exists(Path)

    def Exists(self, aName: str) -> bool:
        '''
        check if file or directory exists.
        '''
        Path = self._FullPath(aName)
        return os.path.exists(Path)

    def ExistsList(self, aFiles: list[str]) -> list[bool]:
        '''
        check if list of file or directory exists.
        '''
        return [os.path.exists(self._FullPath(xFile)) for xFile in aFiles]

    def FileReadStr(self, aName: str) -> str:
        '''
        read text file.
        '''
        Path = self._FullPath(aName)
        with open(Path, 'r', encoding='utf8') as F:
            return F.read()

    async def FileReadChunkPos(self, aName: str, aStreamWriter, aChunkSize: int, aPos: int, aLen: int) -> int:
        '''
        read binary file into sream by chukcs
        '''
        Res = aLen
        Path = self._FullPath(aName)
        with open(Path, 'rb') as F:
            F.seek(aPos)
            while (aLen > 0):
                ChunkSize = min(aChunkSize, aLen)
                Chunk = F.read(ChunkSize)
                if (not Chunk):
                    break

                await aStreamWriter.write(Chunk)
                aLen -= len(Chunk)
        return Res - aLen

    def FileWriteStr(self, aName: str, aData: str) -> int:
        '''
        write text file.
        '''
        self._FullPathCreate(aName)
        Path = self._FullPath(aName)
        with open(Path, 'w', encoding='utf8') as F:
            return F.write(aData)

    async def FileWriteChunkPos(self, aName: str, aStreamReader, aChunkSize: int, aPos: int, aLen: int) -> int:
        '''
        write binary file from sream by chukcs
        '''
        Res = aLen
        self._FullPathCreate(aName)
        Path = self._FullPath(aName)
        Mode = 'r+b' if self.Exists(aName) else 'wb'
        with open(Path, Mode) as F:
            F.seek(aPos)
            while (aLen > 0):
                ChunkSize = min(aChunkSize, aLen)
                Chunk = await aStreamReader.read(ChunkSize)
                if (not Chunk):
                    break

                F.write(Chunk)
                aLen -= len(Chunk)
        return Res - aLen

    def FileTruncate(self, aName: str, aSize: int = 0) -> int:
        '''
        create file or set file size.
        '''
        self._FullPathCreate(aName)
        Path = self._FullPath(aName)
        with open(Path, 'wb') as F:
            F.truncate(aSize)
        return os.path.getsize(Path)

    def List(self, aName: str) -> list:
        '''
        get file list from directory.
        '''
        def WRecurs(aPath: str) -> list:
            nonlocal LenRoot
            Res = []
            for xFile in os.listdir(aPath):
                File = os.path.join(aPath, xFile)
                IsDir = os.path.isdir(File)
                if (IsDir):
                    Res += WRecurs(File)
                Res.append([File[LenRoot:], IsDir])
            return Res

        LenRoot = len(self.Root) + 1
        Path = self._FullPath(aName)
        if (os.path.isdir(Path)):
            R = WRecurs(Path)
            Res = sorted(R, key=lambda x: x[0])
        elif (os.path.isfile(Path)):
            Res = [[aName, False]]
        else:
            Res = [[aName, -1]]
        return Res

    def MassCall(self, aParam: list) -> list:
        '''
        Multiple call in one request.
        aParam = ['DirCreate', ['Dir3/Dir31'], ['Dir4/Dir41']]
        '''
        Res = []
        MethodName, *Param = aParam
        Method = getattr(self, MethodName, None)
        if (Method):
            for xParam in Param:
                try:
                    R = Method(*xParam)
                except Exception as E:
                    R = f'err. {E}'
                Res.append(R)
        else:
            R = [f'err. unknown method {MethodName}']
            Res.append(R)
        return Res

    def MassCalls(self, aParam: list) -> list:
        '''
        Multiple calls in one request.
        aParam = [
            ['DirCreate', ['Dir3/Dir31']],
            ['FileWriteStr', ['file1.txt', '* file1 body *']]
        ]
        '''
        Res = []
        for xMethodName, xParam in aParam:
            Method = getattr(self, xMethodName, None)
            if (Method):
                try:
                    R = Method(*xParam)
                except Exception as E:
                    R = f'err. {E}'
            else:
                R = [f'err. unknown method {xMethodName}']
            Res.append(R)
        return Res

    def Move(self, aSrc: str, aDst: str) -> bool:
        '''
        move/rename file or directory.
        '''
        SrcPath = self._FullPath(aSrc)
        if (os.path.exists(SrcPath)):
            DstPath = self._FullPath(aDst)
            os.rename(SrcPath, DstPath)
            return True

    def Size(self, aName: str) -> int:
        '''
        get size file or directory.
        '''
        def WRecurs(aPath: str) -> int:
            Res = 0
            for xFile in os.listdir(aPath):
                File = os.path.join(aPath, xFile)
                if (os.path.isdir(File)):
                    Res += WRecurs(File)
                else:
                    Res += os.path.getsize(File)
            return Res

        Path = self._FullPath(aName)
        if (os.path.isdir(Path)):
            Res = WRecurs(Path)
        elif (os.path.isfile(Path)):
            Res = os.path.getsize(Path)
        else:
            Res = 0
        return Res
