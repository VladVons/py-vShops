# Created: 2024.12.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import os
from .Common import TFsBase


class TFsDisk(TFsBase):
    def __init__(self, aRoot: str):
        self.Root = aRoot.replace('/', os.sep)

    def _FullPath(self, aPath: str) -> str:
        return f'{self.Root}{os.sep}{aPath.replace('/', os.sep)}'

    def _FullPathCreate(self, aPath: str) -> str:
        Res = aPath.rsplit(os.sep, maxsplit=1)[0] if (os.sep in aPath) else ''
        self.DirCreate(Res)
        return Res

    def DirCreate(self, aName: str) -> bool:
        if (not self.Exists(aName)):
            Path = self._FullPath(aName)
            os.makedirs(Path, exist_ok=False)
            return True

    def Delete(self, aName: str) -> bool:
        def WDirdelete(aPath: str):
            for xFile in os.listdir(aPath):
                File = os.path.join(aPath, xFile)
                if (os.path.isdir(File)):
                    WDirdelete(File)
                    os.rmdir(File)
                else:
                    os.remove(File)

        Path = self._FullPath(aName)
        if (os.path.exists(Path)):
            if (os.path.isdir(Path)):
                WDirdelete(Path)
                os.rmdir(Path)
            else:
                os.remove(Path)
            return not os.path.exists(Path)

    def FileRead(self, aName: str) -> bytes:
        Path = self._FullPath(aName)
        with open(Path, 'rb') as F:
            return F.read()

    def FileWrite(self, aName: str, aData: bytes) -> int:
        assert(isinstance(aData, bytes)), 'expecting bytes'

        self._FullPathCreate(aName)
        Path = self._FullPath(aName)
        with open(Path, 'wb') as F:
            return F.write(aData)

    async def FileReadChunkPos(self, aName: str, aStreamWriter, aChunkSize: int, aPos: int, aLen: int) -> int:
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

    async def FileWriteChunkPos(self, aName: str, aStreamReader, aChunkSize: int, aPos: int, aLen: int) -> int:
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

    def Size(self, aName: str) -> int:
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
        else:
            Res = os.path.getsize(Path)
        return Res

    def Exists(self, aName: str) -> bool:
        Path = self._FullPath(aName)
        return os.path.exists(Path)

    def FileTruncate(self, aName: str, aSize: int = 0) -> int:
        self._FullPathCreate(aName)
        Path = self._FullPath(aName)
        with open(Path, 'wb') as F:
            F.truncate(aSize)
        return os.path.getsize(Path)

    def List(self, aName: str) -> list:
        def WRecurs(aPath: str) -> list:
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
        Res = WRecurs(Path)
        return sorted(Res, key=lambda x: x[0])
