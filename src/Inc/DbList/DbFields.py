# Created: 2022.03.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from .DbErr import TDbListException


class TDbField():
    def __init__(self, aName: str, aType: object, aDef: object = None):
        self.Name = aName
        self.Type = aType
        self.Def = aDef
        self.No = 0

class TDbFields(dict):
    def __init__(self, aFields: tuple = ()):
        super().__init__()

        self.IdxOrd = {}
        self.AddList(aFields)

    def AddField(self, aField: TDbField):
        if (self.get(aField.Name)):
            raise TDbListException('field already exists %s' % (aField.Name))

        if (aField.Def):
            if (not isinstance(aField.Def, aField.Type)):
                raise TDbListException('types mismatch %s, %s' % (aField.Type, aField.Def))
        else:
            Def = {'str': '', 'int': 0, 'float': 0.0, 'bool': False, 'tuple': (), 'list': [], 'dict': {}, 'set': set()}
            aField.Def = Def.get(aField.Type.__name__, object)

        Len = len(self)
        self[aField.Name] = (Len, aField.Type, aField.Def)
        self.IdxOrd[Len] = (aField.Name, aField.Type, aField.Def)

    def Add(self, aName: str, aType: type = str, aDef = None):
        self.AddField(TDbField(aName, aType, aDef))

    def AddList(self, aFields: list):
        for Row in aFields:
            self.Add(*Row)

    def AddAuto(self, aFields: list, aData: list):
        for Idx, Row in enumerate(aFields):
            if (aData):
                if (aData[Idx] is None):
                    Msg = f'TDbFields.AddAuto(). Field {Row} is None'
                    #raise TDbListException(Msg)
                    print(Msg)
                self.Add(Row, type(aData[Idx]))
            else:
                self.Add(Row)

    def Export(self, aWithType: bool = True) -> list:
        if (aWithType):
            Items = sorted(self.items(), key = lambda k: k[1][0])
            Res = [(Key, Type.__name__, Def) for Key, (No, Type, Def) in Items]
        else:
            Res = list(self)
        return Res

    def Import(self, aFields: list):
        Data = [
            # pylint: disable-next=eval-used
            (Name, type(eval(Type)()), Def)
            for Name, Type, Def in aFields
        ]
        self.AddList(Data)

    def GetFields(self, aFields: list[str]) -> 'TDbFields':
        if (not aFields):
            aFields = self.GetList()

        Res = TDbFields()
        for Name in aFields:
            _, Type, Def = self[Name]
            Res.Add(Name, Type, Def)
        return Res

    def GetList(self) -> list:
        return [self.IdxOrd[i][0] for i in range(len(self))]

    def GetNo(self, aName: str) -> int:
        return self[aName][0]
