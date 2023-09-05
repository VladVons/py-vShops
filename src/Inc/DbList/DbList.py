# Created: 2023.02.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from .DbBase import TDbBase
from .DbCond import TDbCond
from .DbRec import TDbRec


class TDbList(TDbBase):
    def __init__(self, aFields: list[str] = None, aData: list = None, aDef: dict = None):
        super().__init__()
        self.Rec = TDbRec()

        if (aFields):
            self.Init(aFields, aData)
            if (aDef):
                self.Rec.Def = aDef

    def _DbExp(self, aData: list, aFields: list[str], aFieldsNew: list[list] = None) -> 'TDbList':
        Res = self.__class__()
        if (aFieldsNew):
            aFields += aFieldsNew

        if (not aFields):
            aFields = self.GetFields()

        Res.Init(aFields, aData)
        return Res

    def _RecInit(self) -> TDbRec:
        self.Rec.Data = self.Data[self._RecNo]
        return self.Rec

    def AddFields(self, aFields: list[str], aValues: list = None):
        for i, x in enumerate(aFields, len(self.Rec.Fields)):
            self.Rec.Fields[x] = i

        if (not aValues):
            Pad = [None] * len(aFields)
            for x in self.Data:
                x += Pad
        else:
            Values = list(zip(*aValues))
            Dif = len(self.Data) - len(Values)
            if (Dif):
                Pad = [None] * len(aFields)
                for i in range(Dif):
                    Values.append(Pad)
            for i, x in enumerate(self.Data):
                self.Data[i] = x + Values[i]
        if (self.Data):
            self._RecInit()

    def Export(self) -> dict:
        '''
        Returns all data in a simple dict for future import
        '''
        Head = list(self.Rec.Fields.keys())
        return {'data': self.Data, 'head': Head, 'tag': self.Tag}

    def GetFieldNo(self, aField: str) -> int:
        return self.Rec.GetFieldNo(aField)

    def GetFields(self) -> list[str]:
        return list(self.Rec.Fields.keys())

    def Import(self, aData: dict) -> 'TDbList':
        if (aData):
            self.Tag = aData.get('tag')

            Head = aData.get('head', [])
            # TDbListSafe fields compatibility
            if (Head) and (isinstance(Head[0], list)):
                Head = [x[0] for x in Head]

            self.Init(Head, aData.get('data'))
        else:
            self.Rec.Fields = {}
            self.Rec.Data = []
            self.Data = []
        return self

    def ImportDbl(self, aDbl: 'TDbList', aFields: list = None, aCond: TDbCond = None, aRecNo: tuple = (0, -1)) -> 'TDbList':
        if (aFields is None):
            aFields = aDbl.GetFields()

        return self.Init(aFields, aDbl.ExportData(aFields, aCond, aRecNo))

    def ImportDict(self, aData: list[dict], aFields: list[str] = None) -> 'TDbBase':
        if (aFields is None):
            aFields = aData[0].keys()

        Data = []
        for xData in aData:
            Row = [xData[Field] for Field in aFields]
            Data.append(Row)
        return self.Init(aFields, Data)

    def Init(self, aFields: list[str], aData: list) -> 'TDbList':
        self.Rec.Init(aFields, aData)

        self._RecNo = 0
        if (aData):
            self.Data = aData
            self._RecInit()
        else:
            self.Rec.Data = []
        return self

    def InitList(self, aField: str, aData: list) -> 'TDbList':
        Data = [[x] for x in aData]
        return self.Init([aField], Data)

    def RecAdd(self, aData: list = None) -> TDbRec:
        if (not aData):
            if (self.Rec.Def):
                aData = [self.Rec.Def.get(x) for x in self.Rec.Fields]
            else:
                aData = [None] * len(self.Rec.Fields)
        else:
            assert(len(aData) == len(self.Rec.Fields)), f'Length mismatch {len(aData)}, {len(self.Rec.Fields)}'
        self.Data.append(aData)
        self._RecNo = self.GetSize() - 1
        return self._RecInit()

    def RecGo(self, aNo: int) -> TDbRec:
        self.RecNo = aNo
        return self.Rec

    def RecPop(self, aRecNo: int = -1) -> TDbRec:
        Res = TDbRec()
        Res.Fields = self.Rec.Fields
        Res.Data = self.Data.pop(aRecNo)
        return Res
