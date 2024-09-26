# Created: 2020.03.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Var.Arr import SortDD


class TDbField(dict):
    def __getattr__(self, aName: str):
        return self.get(aName)

    def ValToData(self, aVal) -> bytearray:
        raise NotImplementedError()

    def DataToVal(self, aVal: bytearray):
        raise NotImplementedError()


class TDbFields(dict):
    Len: int = 0

    def Add(self, aName: str, aType: str, aLen: int):
        raise NotImplementedError()

    def Sort(self, aName: str = 'no'):
        return SortDD(self, aName)

    def Get(self, aName: str) -> TDbField:
        R = self.get(aName)
        assert(R), f'Field not found {aName}'
        return R


class TDb():
    def __init__(self):
        self.S = None   # Stream->S. Abbr for micropython
        self.HeadLen: int = 0
        self.RecLen: int = 0
        self.RecNo: int = 0
        self.RecSave: bool = False
        self.Buf: bytearray = bytearray()
        self.BufFill: bytes = b'\x00'
        self.Fields = None

    def __del__(self):
        self.Close()

    def __iter__(self):
        return self

    def __next__(self):
        if (self.RecNo >= self.GetSize()):
            raise StopIteration

        self.RecGo(self.RecNo)
        self.RecNo += 1
        return self.RecNo - 1

    def _SeekRecNo(self):
        Ofst: int = self.HeadLen + (self.RecNo * self.RecLen)
        self.S.seek(Ofst)

    def _RecRead(self):
        self._SeekRecNo()
        self.Buf = bytearray(self.S.read(self.RecLen))

    def _RecWrite(self):
        if (self.RecSave):
            self.RecSave = False
            self._SeekRecNo()
            self.S.write(self.Buf)
            self._DoRecWrite()

    def _GetFieldData(self, aField: TDbField) -> bytearray:
        return self.Buf[aField.Ofst : aField.Ofst + aField.Len]

    def _SetFieldData(self, aField: TDbField, aData: bytearray):
        self.RecSave = True
        if (aField.Ofst + len(aData) >= len(self.Buf)):
            aData = aData[0:len(self.Buf) - aField.Ofst]
            Len = None
        else:
            Len = aField.Ofst + len(aData) - len(self.Buf)
        self.Buf[aField.Ofst:Len] = aData

    def RecSet(self, aBuf: bytearray):
        assert (len(self.Buf) == len(aBuf)), f'buf len mismatch {len(self.Buf)} {len(aBuf)}'
        self.RecSave = True
        self.Buf = aBuf

    def GetField(self, aName: str):
        Field: TDbField = self.Fields.Get(aName.upper())
        Data = self._GetFieldData(Field)
        return Field.DataToVal(Data)

    def SetField(self, aName: str, aVal):
        Field: TDbField = self.Fields.Get(aName.upper())
        Val = Field.ValToData(aVal)
        self._SetFieldData(Field, Val)

    def GetSize(self) -> int:
        FileSize: int = self.S.seek(0, 2)
        return int((FileSize - self.HeadLen) / self.RecLen)

    def RecGo(self, aNo: int):
        self._RecWrite()
        if (aNo >= 0):
            self.RecNo = min(aNo, self.GetSize())
        else:
            self.RecNo = max(0, self.GetSize() + aNo)
        self._RecRead()

    def RecAdd(self, aCnt: int = 1):
        self._RecWrite()

        self.Buf = bytearray(self.BufFill * self.RecLen)
        self.S.seek(0, 2)
        for _ in range(aCnt):
            self.S.write(self.Buf)
        self.RecNo = self.GetSize() - 1

    def Create(self, aName: str, aFields: TDbFields):
        self.Close()

        self.S = open(aName, 'wb+', encoding = 'utf-8')
        self._StructWrite(aFields)
        self._StructRead()

    def Open(self, aName: str, aROnly: bool = False):
        self.Close()

        Mode: str = 'rb' if aROnly else 'rb+'
        self.S = open(aName, Mode, encoding = 'utf-8')

        #self.HeadLen, self.RecLen
        self._StructRead()

        self.RecGo(0)

    def Close(self):
        if (self.S):
            self._RecWrite()
            self.S.close()
            self.S = None

    def _StructRead(self):
        # init vars self.HeadLen, self.RecLen, self.Fields
        raise NotImplementedError()

    def _StructWrite(self, aFields: TDbFields):
        raise NotImplementedError()

    def _DoRecWrite(self):
        pass
