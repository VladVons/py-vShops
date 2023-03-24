# Created: 2022.03.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from .DbCond import TDbCond
from .DbErr import TDbListException


class TDbRecSafe(list):
    def __init__(self, aParent: 'TDbListSafe'):
        super().__init__()
        self.Parent = aParent

    def __getattr__(self, aName: str) -> object:
        return self.GetField(aName)

    def Find(self, aCond: TDbCond) -> bool:
        return aCond.Find(self)

    def Flush(self):
        ## pylint: disable-next=protected-access
        self.Parent.Data[self.Parent._RecNo] = self.copy()

    def Init(self):
        Fields = self.Parent.Fields
        Rec = [None] * len(Fields)
        for Idx, _ in enumerate(Fields):
            Rec[Idx] = Fields.IdxOrd[Idx][2]
        super().__init__(Rec)

    def GetField(self, aName: str, _aDef: object = None) -> object:
        Idx = self.Parent.Fields.GetNo(aName)
        return self[Idx]

    def SetField(self, aName: str, aValue: object):
        Idx = self.Parent.Fields.GetNo(aName)
        if (self.Parent.OptSafe):
            if (not isinstance(aValue, self.Parent.Fields[aName][1])):
                raise TDbListException('types mismatch %s, %s' % (type(aValue), self.Parent.Fields[aName]))
        self[Idx] = aValue

    def SetData(self, aData: list):
        if (self.Parent.OptSafe):
            if (len(aData) != len(self.Parent.Fields)):
                raise TDbListException('fields count mismatch %s, %s' % (len(aData), len(self.Parent.Fields)))

            if (isinstance(aData, tuple)):
                aData = list(aData)

            IdxOrd = self.Parent.Fields.IdxOrd
            for Idx, FieldD in enumerate(aData):
                if (FieldD is None) and (self.Parent.OptSafeConvert):
                    aData[Idx] = IdxOrd[Idx][2]
                elif (not isinstance(FieldD, IdxOrd[Idx][1])):
                    raise TDbListException('types mismatch %s, %s' % (type(FieldD), IdxOrd[Idx]))
        super().__init__(aData)

    def GetAsDict(self) -> dict:
        return {Key: self[Val[0]] for Key, Val in self.Parent.Fields.items()}

    def GetAsSql(self) -> str:
        Res = []
        for _, (FNo, FType, _) in self.Parent.Fields.items():
            if (isinstance(FType, str)):
                Val = f"'{self[FNo]}'"
            else:
                Val = str(self[FNo])
            Res.append(Val)
        return ', '.join(Res)

    def SetAsDict(self, aData: dict):
        for Key, Val in aData.items():
            self.SetField(Key, Val)
        return self

    def SetAsList(self, aData: list) -> 'TDbRec':
        if (len(aData) - len(self.Parent.Fields)):
            raise TDbListException('rows and fields count mismatch (%s and %s)' % (len(aData), len(self.Parent.Fields)))
        super().__init__(aData)

    def GetAsTuple(self) -> list:
        return [(Key, self[Val[0]]) for Key, Val in self.Parent.Fields.items()]

    def SetAsTuple(self, aData: tuple):
        for Key, Val in aData:
            self.SetField(Key, Val)
        return self

    def SetAsRec(self, aRec: 'TDbRecSafe', aFields: list):
        for Field in aFields:
            self.SetField(Field, aRec.GetField(Field))
        return self

    def SetAsRecTo(self, aRec: 'TDbRecSafe', aFields: dict):
        for From, To in aFields.items():
            self.SetField(To, aRec.GetField(From))
        return self
