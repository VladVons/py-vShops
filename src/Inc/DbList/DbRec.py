# Created: 2022.03.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from .DbCond import TDbCond


class TDbRec():
    def __init__(self):
        self.Data = []
        self.Fields = {}
        self.Def = {}

    def __getattr__(self, aName: str) -> object:
        return self.GetField(aName, self.Def.get(aName))

    def __iter__(self):
        yield from self.Fields.keys()

    def __len__(self):
        return len(self.Fields)

    def __repr__(self) -> str:
        Res = [f'{Key}={Val}' for Key, Val in zip(self.Fields, self.Data)]
        return ', '.join(Res)

    def __setattr__(self, aKey, aVal):
        if (aKey in ('Data', 'Fields', 'Def')):
            super().__setattr__(aKey, aVal)
        else:
            self.SetField(aKey, aVal)

    def _GetFieldsOrder(self) -> list:
        Fields = sorted(self.Fields.items(), key=lambda x: x[1])
        return [x[0] for x in Fields]

    def GetFieldsExtra(self, aFields: list[str]) -> list[str]:
        return set(list(self.Fields)) - set(aFields)

    def GetFieldsMissed(self, aFields: list[str]) -> list[str]:
        return set(aFields) - set(list(self.Fields))

    def Find(self, aCond: TDbCond) -> bool:
        return aCond.Find(self)

    def Flush(self):
        # TDbRecSafe compatibility
        pass

    def GetAsDict(self) -> dict:
        return dict(zip(self.Fields, self.Data))

    def GetAsDictFields(self, aFields: list[str]) -> dict:
        return {xField:self.GetField(xField) for xField in aFields}

    def GetAsDictVal(self) -> dict:
        return {Key:Val for Key, Val in zip(self.Fields, self.Data) if (Val is not None)}

    def GetAsList(self) -> list:
        return self.Data

    def GetAsListFields(self, aFields: list[str]) -> list:
        return [self.GetField(xField) for xField in aFields]

    def GetAsSql(self) -> str:
        Res = [f"'{x}'" if (isinstance(x, str)) else str(x) for x in self.Data]
        return ', '.join(Res)

    def GetAsTuple(self) -> list:
        return list(zip(self.Fields, self.Data))

    def GetAsTupleVal(self) -> dict:
        return ((Key, Val) for Key, Val in zip(self.Fields, self.Data) if (Val is not None))

    def GetField(self, aName: str, aDef = None) -> object:
        Idx = self.Fields.get(aName)
        assert(Idx is not None), f'Field not found {aName}'

        Res = self.Data[Idx]
        if (Res is None):
            Res = aDef
        return Res

    def GetFieldSafe(self, aName: str, aDef = None) -> object:
        Idx = self.Fields.get(aName)
        if (not Idx):
            return aDef

        return self.Data[Idx]

    def GetFieldByNo(self, aNo: int) -> object:
        return self.Data[aNo]

    def GetFieldNo(self, aName: str) -> int:
        Res = self.Fields.get(aName)
        assert(Res is not None), f'Field not found {aName}'
        return Res

    def Init(self, aFields: list, aData: list) -> 'TDbRec':
        self.Fields = {x: i for i, x in enumerate(aFields)}
        if (aData):
            assert(len(aFields) == len(aData[0])), 'length mismatch'
        self.Data = aData
        return self

    def Merge(self, aData: list) -> 'TDbRec':
        assert(len(self) == len(self.Data) + len(aData)), 'Size mismatch'
        self.Data.extend(aData)
        return self

    def RenameFields(self, aOld: list[str], aNew: list[str]):
        for Old, New in zip(aOld, aNew):
            assert (Old in self.Fields), f'Field not found {Old}'
            self.Fields[New] = self.Fields.pop(Old)
        self.Fields = {Val:Idx for Idx, Val in enumerate(self._GetFieldsOrder())}

    def SetAsDict(self, aData: dict) -> 'TDbRec':
        for Key, Val in aData.items():
            self.SetField(Key, Val)
        return self

    def SetAsList(self, aData: list) -> 'TDbRec':
        Diff = len(aData) - len(self.Fields)
        if (Diff != 0):
            if (Diff < 0):
                aData += [None] * abs(Diff)
            else:
                aData = aData[:-Diff]
        # pylint: disable-next=unnecessary-dunder-call
        self.Data.__init__(aData)

    def SetAsRec(self, aRec: 'TDbRec', aFields: list[str]) -> 'TDbRec':
        for Field in aFields:
            self.SetField(Field, aRec.GetField(Field))
        return self

    def SetAsRecTo(self, aRec: 'TDbRec', aFields: dict):
        for From, To in aFields.items():
            self.SetField(To, aRec.GetField(From))
        return self

    def SetAsTuple(self, aData: tuple) -> 'TDbRec':
        for Key, Val in aData:
            self.SetField(Key, Val)
        return self

    def SetField(self, aName: str, aValue: object) -> 'TDbRec':
        Idx = self.Fields.get(aName)
        assert(Idx is not None), f'Field not found {aName}'

        self.Data[Idx] = aValue
        return self
