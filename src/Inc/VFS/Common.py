# Created: 2024.12.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


class TFsBase():
    def Copy(self, aSrc: str, aDst: str) -> bool:
        raise NotImplementedError()

    def Delete(self, aName: str) -> bool:
        raise NotImplementedError()

    def DirCreate(self, aName: str):
        raise NotImplementedError()

    def Exists(self, aName: str) -> bool:
        raise NotImplementedError()

    def FileReadStr(self, aName: str) -> str:
        raise NotImplementedError()

    async def FileReadChunkPos(self, aName: str, aStreamWriter, aChunkSize: int, aPos: int, aLen: int) -> int:
        raise NotImplementedError()

    def FileTruncate(self, aName: str, aSize: int = 0) -> int:
        raise NotImplementedError()

    def FileWriteStr(self, aName: str, aData: str) -> int:
        raise NotImplementedError()

    async def FileWriteChunkPos(self, aName: str, aStreamReader, aChunkSize: int, aPos: int, aLen: int) -> int:
        raise NotImplementedError()

    def List(self, aName: str) -> list:
        raise NotImplementedError()

    def Size(self, aName: str) -> int:
        raise NotImplementedError()
