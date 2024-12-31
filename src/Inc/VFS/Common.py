# Created: 2024.12.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


class TFsBase():
    def Delete(self, aName: str) -> bool:
        raise NotImplementedError()

    def DirCreate(self, aName: str):
        raise NotImplementedError()

    def Exists(self, aName: str) -> bool:
        raise NotImplementedError()

    def FileRead(self, aName: str) -> bytes:
        raise NotImplementedError()

    def FileWrite(self, aName: str, aData: bytes) -> int:
        raise NotImplementedError()

    async def FileReadChunkPos(self, aName: str, aStreamWriter, aChunkSize: int, aPos: int, aLen: int) -> int:
        raise NotImplementedError()

    async def FileWriteChunkPos(self, aName: str, aStreamReader, aChunkSize: int, aPos: int, aLen: int) -> int:
        raise NotImplementedError()

    def List(self, aName: str) -> list:
        raise NotImplementedError()

    def Size(self, aName: str) -> int:
        raise NotImplementedError()
