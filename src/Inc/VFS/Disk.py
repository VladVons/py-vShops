# Created: 2024.12.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import os
from . import TFsBase


class TFsDisk(TFsBase):
    def __init__(self, aRoot: str):
        self.Root = aRoot.replace('/', os.sep)

    def _FullPath(self, aPath: str) -> str:
        return f'{self.Root}{os.sep}{aPath.replace('/', os.sep)}'

    def DirCreate(self, aName: str):
        if (not self.FileExists(aName)):
            Path = self._FullPath(aName)
            os.makedirs(Path, exist_ok=False)

    def FileRead(self, aName: str) -> bytes:
        Path = self._FullPath(aName)
        with open(Path, 'rb') as F:
            return F.read()

    def FileWrite(self, aName: str, aData: bytes) -> int:
        assert(isinstance(aData, bytes)), 'expecting bytes'

        Path = self._FullPath(aName)
        with open(Path, 'wb') as F:
            return F.write(aData)

    async def FileReadChunk(self, aName: str, aStreamWriter, aChunkSize: int):
        Path = self._FullPath(aName)
        with open(Path, 'rb') as F:
            while xChunk := F.read(aChunkSize):
                await aStreamWriter.write(xChunk)

    async def FileWriteChunk(self, aName: str, aStreamReader, aChunkSize: int):
        Path = self._FullPath(aName)
        with open(Path, 'wb') as F:
            while xChunk := await aStreamReader.read(aChunkSize):
                F.write(xChunk)

    def FileDelete(self, aName: str):
        if (self.FileExists(aName)):
            Path = self._FullPath(aName)
            os.remove(Path)

    def FileSize(self, aName: str) -> int:
        Path = self._FullPath(aName)
        return os.path.getsize(Path)

    def FileExists(self, aName: str) -> bool:
        Path = self._FullPath(aName)
        return os.path.exists(Path)
