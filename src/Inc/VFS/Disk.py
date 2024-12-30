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
        if (not self.FileExists(aName)):
            Path = self._FullPath(aName)
            os.makedirs(Path, exist_ok=False)
            return True

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

    async def FileReadChunk(self, aName: str, aStreamWriter, aChunkSize: int):
        Path = self._FullPath(aName)
        with open(Path, 'rb') as F:
            while xChunk := F.read(aChunkSize):
                await aStreamWriter.write(xChunk)

    async def FileReadChunkPos(self, aName: str, aStreamWriter, aChunkSize: int, aPos: int, aLen: int) -> int:
        Res = aLen

        Path = self._FullPath(aName)
        with open(Path, 'rb') as F:
            F.seek(aPos)
            while aLen > 0:
                ChunkSize = min(aChunkSize, aLen)
                Chunk = F.read(ChunkSize)
                if (not Chunk):
                    break

                await aStreamWriter.write(Chunk)
                aLen -= len(Chunk)
        return Res - aLen

    async def FileWriteChunk(self, aName: str, aStreamReader, aChunkSize: int):
        Res = 0
        self._FullPathCreate(aName)
        Path = self._FullPath(aName)
        with open(Path, 'wb') as F:
            while xChunk := await aStreamReader.read(aChunkSize):
                Res += F.write(xChunk)
        return Res

    async def FileWriteChunkPos(self, aName: str, aStreamReader, aChunkSize: int, aPos: int, aLen: int) -> int:
        Res = aLen
        self._FullPathCreate(aName)
        Path = self._FullPath(aName)
        Mode = 'r+b' if self.FileExists(aName) else 'wb'
        with open(Path, Mode) as F:
            F.seek(aPos)
            while aLen > 0:
                ChunkSize = min(aChunkSize, aLen)
                Chunk = await aStreamReader.read(ChunkSize)
                if (not Chunk):
                    break

                F.write(Chunk)
                aLen -= len(Chunk)
        return Res - aLen

    def FileDelete(self, aName: str) -> bool:
        if (self.FileExists(aName)):
            Path = self._FullPath(aName)
            os.remove(Path)
            return True

    def FileSize(self, aName: str) -> int:
        Path = self._FullPath(aName)
        return os.path.getsize(Path)

    def FileExists(self, aName: str) -> bool:
        Path = self._FullPath(aName)
        return os.path.exists(Path)

    def Truncate(self, aName: str, aSize: int = 0) -> int:
        self._FullPathCreate(aName)
        Path = self._FullPath(aName)
        with open(Path, 'wb') as F:
            F.truncate(aSize)
        return os.path.getsize(Path)

    def List(self, aName: str) -> list:
        Files = []
        LenRoot = len(self.Root) + 1
        Path = self._FullPath(aName)
        for xRoot, _xDirs, xFiles in os.walk(Path):
            for xFile in xFiles:
                File = xRoot[LenRoot:] + os.sep + xFile
                Files.append(File)
        return Files
