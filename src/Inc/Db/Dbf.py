# Created: 2020.02.29
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import struct
import time
#
from .Db import TDb, TDbFields, TDbField


class TDbfField(TDbField):
    def _DefLen(self, aType: str, aLen: int) -> int:
        if (aLen == 0):
            aLen = {'C': 10, 'N': 10, 'D': 8, 'L': 1}.get(aType, 0)
        return aLen

    def ValToData(self, aVal) -> bytearray:
        if (self.Type == 'L'):
            aVal = 'T' if aVal else 'F'
        elif (self.Type == 'D'):
            lt = time.localtime(aVal)
            aVal = '%04d%02d%02d' % (lt[0], lt[1], lt[2])
        else:
            aVal = str(aVal)
        return aVal.encode()

    def DataToVal(self, aVal: bytearray):
        aVal: str = aVal.decode().strip()

        if (self.Type == 'N'):
            if (self.LenD > 0):
                aVal = float(aVal if aVal != '' else '0.0')
            else:
                aVal = int(aVal if aVal != '' else '0')
        elif (self.Type == 'F'):
            aVal = float(aVal if aVal != '' else '0.0')
        elif (self.Type == 'L'):
            aVal = (aVal == 'T')
        elif (self.Type == 'D'):
            if (aVal == ''):
                aVal = '20010101'
            #R = time.mktime([int(R[0:4]), int(R[4:6]), int(R[6:8]), 0, 0, 0, 0, 0])
        return aVal


class TDbfFields(TDbFields):
    def Add(self, aName: str, aType: str, aLen: int = 0, aLenD: int = 0) -> TDbfField:
        aName = aName.upper()
        aType = aType.upper()

        R: TDbfField = TDbfField()
        aLen = R._DefLen(aType, aLen)
        R.update({'name': aName, 'type': aType, 'len': aLen, 'no': len(self), 'ofst': self.Len, 'len_d': aLenD})
        self[aName] = R
        self.Len += aLen
        return R


class TDbf(TDb):
    Sign: int = 3

    def __init__(self):
        super().__init__()
        self.BufFill = b' '

    def _StructRead(self):
        self.S.seek(0)
        Data = self.S.read(32)
        Sign, _LUpd, _RecCnt, self.HeadLen, self.RecLen = struct.unpack('<1B3s1I1H1H', Data[0:1+3+4+2+2])
        assert (Sign == self.Sign), 'bad signature'

        self.Fields = TDbfFields()
        self.Fields.Add('del', 'C', 1, 0)

        self.S.seek(32)
        while True:
            Data = self.S.read(32)
            if (Data[0] == 0x0D):
                break

            FName, FType, _X, FLen, FLenD = struct.unpack('<11s1s4s1B1B', Data[0:11+1+4+1+1])
            Name = FName.split(b'\x00', 1)[0].decode()
            self.Fields.Add(Name, FType.decode(), FLen, FLenD)

    def _StructWrite(self, aFields: TDbfFields):
        RecLen: int  = aFields.Len + 1
        HeadLen: int = 32 + (32 * len(aFields)) + 1
        Data = struct.pack('<1B3B1I1H1H', self.Sign, 1, 1, 1, 0, HeadLen, RecLen)
        self.S.seek(0)
        self.S.write(Data)

        self.S.seek(32)
        for _K, V in aFields.Sort():
            Data = struct.pack('<11s1s4s1B1B14s', V.Name.encode(), V.Type.encode(), b'\x00', V.Len, V.LenD, b'\x00')
            self.S.write(Data)
        self.S.write(b'\x0D')

    def _DoRecWrite(self):
        # YYMMDD, RecCount
        Data = struct.pack('<1B1B1B1I', 20, 1, 1, self.GetSize())
        self.S.seek(1)
        self.S.write(Data)

    def RecDelete(self, aMode: bool = True):
        self.RecSave = True
        self.Buf[0] = 42 if aMode else 32

    def RecDeleted(self) -> bool:
        return self.Buf[0] == 42
