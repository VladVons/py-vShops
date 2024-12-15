# Created: 2024.12.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import os
from . import TFsBase


class TFsMem(TFsBase):
    def __init__(self):
        self.Data = {}

    @staticmethod
    def _SplitPath(aPath: str) -> list[str]:
        return aPath.split(os.sep)

    def _GetChainNested(self, aPath: str) -> dict:
        Data = self.Data
        Keys = self._SplitPath(aPath)
        for xKey in Keys[:-1]:
            if (isinstance(Data, dict)):
                Data = Data.get(xKey)
                if (Data is None):
                    return
            else:
                return
        return (Data, Keys[-1])

    def _GetValueNested(self, aPath: str, aDef = None) -> object:
        Data = self.Data
        for xKey in self._SplitPath(aPath):
            if (isinstance(Data, dict)):
                Data = Data.get(xKey)
                if (Data is None):
                    return aDef
            else:
                return aDef
        return Data

    def _SetValueNested(self, aPath: str, aValue: object) -> dict:
        aData = self.Data
        Keys = self._SplitPath(aPath)
        for xKey in Keys[:-1]:
            if (xKey):
                Data = aData.get(xKey)
                if (Data is None):
                    aData[xKey] = Data = {}
                aData = Data
        aData[Keys[-1]] = aValue
        return aData

    def DirCreate(self, aName: str):
        self._SetValueNested(aName, None)

    def FileRead(self, aName: str) -> bytes:
        return self._GetValueNested(aName)

    def FileWrite(self, aName: str, aData: bytes) -> int:
        assert(isinstance(aData, bytes)), 'expecting bytes'

        self._SetValueNested(aName, aData)
        return len(aData)

    async def FileReadChunk(self, aName: str, aStreamWriter, aChunkSize: int):
        Data = self.FileRead(aName)
        for i in range(0, len(Data), aChunkSize):
            Chunk = Data[i:i + aChunkSize]
            await aStreamWriter.write(Chunk)

    async def FileWriteChunk(self, aName: str, aStreamReader, aChunkSize: int):
        Data = b''
        while xChunk := await aStreamReader.read(aChunkSize):
            Data += xChunk
        self.FileWrite(aName, Data)

    def FileDelete(self, aName: str):
        if (self.FileExists(aName)):
            Data, Key = self._GetChainNested(aName)
            del Data[Key]

    def FileSize(self, aName: str) -> int:
        Data = self._GetValueNested(aName)
        return (len(Data))

    def FileExists(self, aName: str) -> bool:
        return self._GetValueNested(aName) is not None
