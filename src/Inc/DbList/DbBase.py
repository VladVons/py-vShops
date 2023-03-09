# Created: 2023.02.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import random
import json
#
from .BeeTree import TBeeTree
from .DbCond import TDbCond
from .DbErr import TDbListException


class TDbBase():
    def __init__(self):
        self.Data = []
        self.Tag = 0
        self._RecNo = 0
        self.BeeTree = {}
        self.OptReprLen = 25

    def __len__(self):
        return self.GetSize()

    def __iter__(self):
        self._RecNo = -1
        return self

    def __next__(self):
        if (self._RecNo >= self.GetSize() - 1):
            raise StopIteration

        self._RecNo += 1
        return self._RecInit()

    def __repr__(self) -> str:
        return self._Repr()

    def _DbExp(self, aData: list, aFields: list[str], aFieldsNew: list[list] = None) -> 'TDbBase':
        raise NotImplementedError()

    def _RecInit(self) -> object:
        raise NotImplementedError()

    def _Repr(self) -> str:
        def _GetMaxLen() -> list:
            nonlocal Fields

            Res = [len(x) for x in Fields]

            for Row in self.Data:
                for Idx, Val in enumerate(Row):
                    Res[Idx] = max(Res[Idx], len(str(Val).strip()))

            for Idx, _ in enumerate(Res):
                Res[Idx] = min(Res[Idx], self.OptReprLen)

            return Res

        Fields = self.GetFields()
        FieldsLen = _GetMaxLen()

        if (self.Data):
            Format = []
            for Idx, x in enumerate(self.Data[0]):
                Align = '' if x in [int, float] else '-'
                Format.append('%' + Align + str(FieldsLen[Idx]) + 's\t')
        else:
            Format = [f'%{x}s\t' for x in FieldsLen]
        Format = ''.join(Format)

        Res = []
        Res.append(Format % tuple(Fields))
        for Idx, Row in enumerate(self.Data):
            Trimmed = []
            for x in Row:
                x = str(x)
                if (len(x) > self.OptReprLen):
                    x = x[:self.OptReprLen - 3] + '...'
                Trimmed.append(x)
            Res.append(Format % tuple(Trimmed))
        Res.append(f'records: {self.GetSize()}')
        return '\n'.join(Res)

    def _Group(self, aFieldsUniq: list[str], aFieldsSum: list[str]) -> dict:
        Res = {}

        FieldsNoUniq = [self.GetFieldNo(x) for x in aFieldsUniq]
        FieldsNoSum = [self.GetFieldNo(x) for x in aFieldsSum]

        for Row in self.Data:
            FKey = tuple(Row[x] for x in FieldsNoUniq)
            if (FKey not in Res):
                Res[FKey] = []
            FSum = [Row[x] for x in FieldsNoSum]
            Res[FKey].append(FSum)
        return Res

    def Append(self, aDbl: list['TDbBase']) -> 'TDbBase':
        for x in aDbl:
            self.Data += x.Data
        return self

    def Clone(self, aFields: list[str] = None, aCond: TDbCond = None, aRecNo: tuple = None) -> 'TDbBase':
        if (aFields is None):
            aFields = []
        if (aRecNo is None):
            aRecNo = (0, -1)

        Data = self.ExportData(aFields, aCond, aRecNo)
        return self._DbExp(Data, aFields)

    def DelField(self, aField: str) -> list[str]:
        FieldNo = self.GetFieldNo(aField)
        for Row in self.Data:
            del Row[FieldNo]

        Fields = self.GetFields()
        Fields.remove(aField)
        return Fields

    def GetFieldNo(self, aField: str) -> int:
        raise NotImplementedError()

    def Empty(self):
        self.Data = []
        self._RecNo = 0

    def Export(self) -> dict:
        raise NotImplementedError()

    def ExportData(self, aFields: list = None, aCond: TDbCond = None, aRecNo: tuple = None) -> list:
        if (aFields is None):
            aFields = []
        if (aRecNo is None):
            aRecNo = (0, -1)

        Start, Finish = aRecNo
        if (Finish == -1):
            Finish = self.GetSize()

        if (aFields):
            FieldsNo = [self.GetFieldNo(x) for x in aFields]
        else:
            aFields = self.GetFields()
            FieldsNo = list(range(len(aFields)))

        if (aCond):
            Data = [[Val[i] for i in FieldsNo] for Val in self.Data[Start:Finish] if aCond.Find(Val)]
        else:
            #return [list(map(i.__getitem__, FieldsNo)) for i in self.Data[Start:Finish]]
            Data = [[Val[i] for i in FieldsNo] for Val in self.Data[Start:Finish]]
        return Data

    def ExportList(self, aField: str, aUniq = False) -> list:
        '''
        Returns one field as list
        '''
        FieldNo = self.GetFieldNo(aField)
        Res = [x[FieldNo] for x in self.Data]
        if (aUniq):
            Res = list(set(Res))
        return Res

    def ExportPair(self, aFieldKey: str, aFieldVal: str) -> dict:
        '''
        Returns two binded fields as key:val
        '''
        KeyNo = self.GetFieldNo(aFieldKey)
        ValNo = self.GetFieldNo(aFieldVal)
        return {x[KeyNo]: x[ValNo] for x in self.Data}

    def GetDiff(self, aField: str, aList: list) -> tuple:
        Set1 = set(self.ExportList(aField))
        Set2 = set(aList)
        return (Set1 - Set2, Set2 - Set1)

    def GetFields(self) -> list[str]:
        raise NotImplementedError()

    def GetSize(self) -> int:
        return len(self.Data)

    def Group(self, aFieldsUniq: list[str], aFieldsSum: list[str] = None) -> 'TDbBase':
        if (aFieldsSum is None):
            aFieldsSum = []

        Grouped = self._Group(aFieldsUniq, aFieldsSum)
        Data = []
        for Key, Val in Grouped.items():
            ZipVal = zip(*Val)
            Row = list(Key) + [sum(i) for i in ZipVal] + [len(Val)]
            Data.append(Row)

        # FieldsSum = [(Key + '_Sum', Val[1]) for Key, Val in self.Fields.GetFields(aFieldsSum).items()]
        # return self._DbExp(Data, aFieldsUniq, FieldsSum + [('count', int)])
        return self._DbExp(Data, aFieldsUniq + aFieldsSum, [('count', int)])

    def Find(self, aCond: TDbCond) -> int:
        for i in range(self._RecNo, self.GetSize()):
            if (aCond.Find(self.Data[i])):
                return i
        return -1

    def FindField(self, aName: str, aValue) -> int:
        FieldNo = self.GetFieldNo(aName)
        for i in range(self._RecNo, self.GetSize()):
            if (self.Data[i][FieldNo] == aValue):
                return i
        return -1

    def Import(self, aData: dict) -> 'TDbBase':
        raise NotImplementedError()

    def IsEmpty(self) -> bool:
        return (self.GetSize() == 0)

    def Load(self, aFile: str) -> 'TDbBase':
        with open(aFile, 'r', encoding = 'utf-8') as F:
            Data = json.load(F)
            self.Import(Data)
            return self

    def New(self) -> 'TDbBase':
        return self._DbExp([], [])

    @property
    def RecNo(self) -> int:
        return self._RecNo

    @RecNo.setter
    def RecNo(self, aNo: int):
        Size = self.GetSize()
        if (Size == 0):
            self._RecNo = 0
        else:
            if (aNo < 0):
                aNo = Size + aNo
            self._RecNo = min(aNo, Size - 1)
        self._RecInit()

    def Save(self, aFile: str, aFormat: bool = False):
        with open(aFile, 'w', encoding = 'utf-8') as F:
            Data = self.Export()
            if (aFormat):
                json.dump(Data, F, indent=2, sort_keys=True, ensure_ascii=False)
            else:
                json.dump(Data, F)

    def Search(self, aField: str, aVal) -> int:
        if (aField not in self.BeeTree):
            raise TDbListException('SearchAdd()')
        return self.BeeTree[aField].Search(aVal)

    def SearchAdd(self, aField: str, aAllowEmpty: bool = False) -> TBeeTree:
        BeeTree = TBeeTree()
        FieldNo = self.GetFieldNo(aField)
        for RowNo, Row in enumerate(self.Data):
            Data = Row[FieldNo]
            if (Data or aAllowEmpty):
                BeeTree.Add((Data, RowNo))
        self.BeeTree[aField] = BeeTree
        return BeeTree

    def Sort(self, aFields: list[str], aReverse: bool = False) -> 'TDbBase':
        if (len(aFields) == 1):
            FieldNo = self.GetFieldNo(aFields[0])
            self.Data.sort(key=lambda x: (x[FieldNo]), reverse=aReverse)
        else:
            F = ''
            for Field in aFields:
                F += 'x[%s],' % self.GetFieldNo(Field)
            Script = 'self.Data.sort(key=lambda x: (%s), reverse=%s)' % (F, aReverse)
            # pylint: disable-next=eval-used
            eval(Script)
        self.RecNo = 0
        return self

    def Shuffle(self) -> 'TDbBase':
        random.shuffle(self.Data)
        self.RecNo = 0
        return self
