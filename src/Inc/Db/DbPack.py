# Created: 2020.03.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import struct
#
from .Db import TDb, TDbFields, TDbField


class TDblField(TDbField):
    def Struct(self) -> str:
        if (self.Type == 's'):
            Res = '%s%s' % (self.Len, 's')
        else:
            Res = '%s%s' % (1, self.Type)
        return Res

    def ValToData(self, aVal) -> bytearray:
        Struct: str = '<' + self.Struct()
        if (self.Type == 's'):
            Res = struct.pack(Struct, aVal.encode())
        else:
            Res = struct.pack(Struct, aVal)
        return Res

    def DataToVal(self, aVal: bytearray):
        Struct: str = '<' + self.Struct()
        if (self.Type == 's'):
            Data = struct.unpack(Struct, aVal)
            R = Data[0].split(b'\x00', 1)[0].decode()
        else:
            Data = struct.unpack(Struct, aVal)
            R = Data[0]
        return R


class TDblFields(TDbFields):
    def Add(self, aName: str, aType: str, aLen: int = 1) -> TDblField:
        aName = aName.upper()

        if (aType != 's'):
            aLen = 1
        Len: int = struct.calcsize('<%s%s' % (aLen, aType))

        R = TDblField()
        R.update({'name': aName, 'type': aType, 'len': Len, 'no': len(self), 'ofst': self.Len})
        self[aName] = R
        self.Len += Len
        return R

    def Struct(self) -> str:
        R: str = '<'
        for K, _ in self.Sort():
            R += self[K].Struct()
        return R


class TDbPack(TDb):
    Sign: int = 71

    def _StructWrite(self, aFields: TDblFields):
        HeadLen: int = 16 + (16 * len(aFields))
        Data = struct.pack('<1B1H1H1H', self.Sign, HeadLen, aFields.Len, len(aFields))
        self.S.seek(0)
        self.S.write(Data)

        self.S.seek(16)
        for _K, V in aFields.Sort():
            Data = struct.pack('<11s1s1B3s', V.Name.encode(), V.Type.encode(), V.Len, b'\x00')
            self.S.write(Data)

    def _StructRead(self):
        self.Fields = TDblFields()

        self.S.seek(0)
        Data = self.S.read(16)
        Sign, self.HeadLen, self.RecLen, Fields = struct.unpack('<1B1H1H1H', Data[0:1+2+2+2])
        assert (Sign == self.Sign), 'bad signature'

        for _i in range(Fields):
            Data = self.S.read(16)
            FName, FType, FLen, _X = struct.unpack('<11s1s1B3s', Data)
            Name = FName.split(b'\x00', 1)[0].decode()
            self.Fields.Add(Name, FType.decode(), FLen)
