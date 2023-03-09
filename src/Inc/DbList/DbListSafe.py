# Created: 2022.03.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from .DbBase import TDbBase
from .DbCond import TDbCond
from .DbErr import TDbListException
from .DbFields import TDbFields
from .DbRecSafe import TDbRecSafe


class TDbListSafe(TDbBase):
    def __init__(self, aFields: list = None, aData: list = None):
        super().__init__()

        self.Fields = None
        if (aFields is None):
            aFields = []

        self.OptSafe = True
        self.OptSafeConvert = True

        self.Rec = TDbRecSafe(self)
        self.Init(aFields, aData)

    def _DbExp(self, aData: list, aFields: list[str], aFieldsNew: list[list] = None) -> 'TDbListSafe':
        Res = self.__class__()
        Res.Fields = self.Fields.GetFields(aFields)
        if (aFieldsNew):
            Res.Fields.AddList(aFieldsNew)
        Res.Data = aData
        return Res

    def _RecInit(self) -> TDbRecSafe:
        if (not self.IsEmpty()):
            self.Rec.SetData(self.Data[self._RecNo])
        return self.Rec

    def AddFields(self, aFields: list = None):
        if (aFields is None):
            aFields = []

        self.Fields.AddList(aFields)
        for Row in self.Data:
            for Field in aFields:
                Def = self.Fields[Field[0]][2]
                Row.append(Def)

    def DelField(self, aField: str):
        Fields = super().DelField(aField)
        self.Fields = self.Fields.GetFields(Fields)

    def Export(self) -> dict:
        '''
        Returns all data in a simple dict for future import
        '''
        return {'data': self.Data, 'head': self.Fields.Export(), 'tag': self.Tag}

    def ExportDict(self) -> list:
        return [Rec.GetAsDict() for Rec in self]

    def GetFieldNo(self, aField: str) -> int:
        return self.Fields.GetNo(aField)

    def GetFields(self) -> list[str]:
        return self.Fields.keys()

    def Import(self, aData: dict) -> 'TDbListSafe':
        self.Tag = aData.get('tag')
        self.Fields = TDbFields()
        self.Data = aData.get('data', [])
        self.Fields.Import(aData.get('head'))
        self.RecNo = 0
        return self

    def ImportAutoFields(self, aData: list, aFields: list[str]) -> 'TDbListSafe':
        if (not aData):
            raise TDbListException('Cant auto import empty data')

        self.Data = aData
        self.Fields.AddAuto(aFields, aData[0])
        self.RecNo = 0
        return self

    def ImportList(self, aField: str, aData: list):
        Rec = TDbRecSafe(self)
        Rec.Init()
        FieldNo = self.Fields.GetNo(aField)
        for Row in aData:
            Arr = Rec.copy()
            Arr[FieldNo] = Row
            self.Data.append(Arr)

    def ImportDbl(self, aDbl: 'TDbListSafe', aFields: list = None, aCond: TDbCond = None, aRecNo: tuple = (0, -1)) -> 'TDbListSafe':
        if (aFields is None):
            aFields = []

        self.Data = aDbl.ExportData(aFields, aCond, aRecNo)
        self.Fields = aDbl.Fields.GetFields(aFields)
        self.Tag = aDbl.Tag
        return self

    def ImportPair(self, aData: dict, aKeyName: str, aFieldValue: tuple) -> 'TDbListSafe':
        self.Fields = TDbFields([(aKeyName, str), aFieldValue])
        self.Data = [[Key, Val] for Key, Val in aData.items()]
        return self

    def Init(self, aFields: list, aData: list = None):
        self.Fields = TDbFields()
        self.Fields.AddList(aFields)
        self.SetData(aData)

    def InitList(self, aField: tuple, aData: list):
        self.Fields = TDbFields()
        self.Fields.Add(*aField)
        self.ImportList(aField[0], aData)

    def RecGo(self, aNo: int) -> TDbRecSafe:
        self.RecNo = aNo
        return self.Rec

    def RecAdd(self, aData: list = None) -> TDbRecSafe:
        if (aData):
            self.Rec.SetData(aData)
        else:
            self.Rec.Init()
        self.Data.append(self.Rec.copy())
        self._RecNo = self.GetSize() - 1
        return self.Rec

    def RecPop(self, aRecNo: int = -1) -> TDbRecSafe:
        Res = TDbRecSafe(self)
        Res.SetData(self.Data.pop(aRecNo))
        return Res

    def SetData(self, aData: list):
        if (aData):
            if (len(aData[0]) != len(self.Fields)):
                raise TDbListException('rows and fields count mismatch (%s and %s)' % (len(aData[0]), len(self.Fields)))

            if (self.OptSafe):
                for x in aData:
                    self.RecAdd(x)
            else:
                self.Data = aData
            self.RecNo = 0
        else:
            self.Empty()
