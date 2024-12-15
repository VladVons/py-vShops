# Created: 2024.12.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


class TFsBase():
    def DirCreate(self, aName: str):
        raise NotImplementedError()

    def FileRead(self, aName: str) -> bytes:
        raise NotImplementedError()

    def FileWrite(self, aName: str, aData: bytes) -> int:
        raise NotImplementedError()

    def FileDelete(self, aName: str):
        raise NotImplementedError()

    def FileSize(self, aName: str) -> int:
        raise NotImplementedError()

    def FileExists(self, aName: str) -> bool:
        raise NotImplementedError()
