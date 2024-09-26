import os
import json
#
from Inc.Var.Dict import DeepGet
from Inc.Var.DictEx import DeepGetsRe
from Inc.Misc.FS import DirWalk


class TPgMeta():
    @staticmethod
    def _ForeignKey(aColumn: str, aTableF: str, aColumnF) -> str:
        return f'foreign key ({aColumn}) references {aTableF}({aColumnF})'

    @staticmethod
    def AddTable(aTable: str, aBody: str = '') -> str:
        return f'create table if not exists {aTable}({aBody});'

    @staticmethod
    def AddTableMeta(aName: str, aMeta: dict) -> str:
        Body = []

        for Key, Val in aMeta.get('column', {}).items():
            Value = Val.get("value", "")
            if (DeepGet(aMeta, f'foreign_key.{Key}')):
                if ('not null' not in Value):
                    Value += ' not null'
            Body.append(f'{Key:16} {Val.get("type")} {Value}')

        for Key, Val in aMeta.get('foreign_key', {}).items():
            Body.append(TPgMeta._ForeignKey(Key, Val.get("table"), Val.get("column")))

        for Key, Val in aMeta.get('index', {}).items():
            if (Val.get('type') == 'primary'):
                Body.append(f'primary key ({Key})')

        Body = [x.strip() for x in Body]
        Res = TPgMeta.AddTable(aName, '\n  %s\n' % (',\n  '.join(Body)))

        if ('comment' in aMeta):
            Res += '\n' + TPgMeta.AddTableComment(aName, aMeta['comment'])
        return Res

    @staticmethod
    def AddTableComment(aName: str, aComment: str) -> str:
        return f'comment on table {aName} is "{aComment}";'

    @staticmethod
    def AddColumn(aTable: str, aColumn: str, aType: str) -> str:
        return f'alter table {aTable} add column {aColumn} {aType};'

    @staticmethod
    def AddIndex(aTable: str, aColumn: list[str], aType: str = '') -> str:
        Columns = ', '.join(aColumn)
        if (aType in ['', 'unique']):
            Name = aTable + '_'.join(aColumn) + '_idx'
            Res = f'create {aType} index {Name} on {aTable} ({Columns});'
        elif (aType == 'primary'):
            Res = f'alter table {aTable} add primary key ({Columns});'
        return Res


class TDbMeta():
    def __init__(self, aDir: str):
        self.Dir = aDir
        self.Tables = []

        self.Data = {}
        self.Refers = {}
        self.Keys = {}
        self._InitData()

    def _GetDirs(self) -> list[str]:
        return [x[0] for x in DirWalk(self.Dir, '.*', 'd', 1)]

    def _InitData(self):
        for Dir in self._GetDirs():
            Name = os.path.basename(Dir)
            File = f'{Dir}/Meta.json'
            with open(File, 'r', encoding='UTF8') as F:
                self.Data[Name] = json.load(F)
            Items = DeepGetsRe(self.Data[Name], ['table', '.*', 'foreign_key', '.*', 'table'])
            for Foreign, Path in Items:
                Master = Path.split('.')[1]
                self.Refers[Foreign] = self.Refers.get(Foreign, []) + [Master]
                self.Keys[Master] = self.Keys.get(Master, []) + [Foreign]

    def _FindTable(self, aName: str) -> tuple:
        for Key, Val in self.Data.items():
            Res = DeepGet(Val, f'table.{aName}')
            if (Res):
                return (Key, Res)

    def _LoadTable(self, aName: str):
        if (aName in self.Tables):
            return

        Table = self._FindTable(aName)
        if (Table):
            self.Tables.append(aName)

            ForeignKey = Table[1].get('foreign_key', {})
            for _ForeignK, ForeignD in ForeignKey.items():
                ForeignTable = ForeignD['table']
                self._LoadTable(ForeignTable)
                for RefersD in self.Refers.get(ForeignTable, []):
                    self._LoadTable(RefersD)
        else:
            print(f' Table not found {aName}')

    def Sort(self) -> list:
        ResSort = []

        def SearchLastPos(aTable: str) -> int:
            Res = 0
            for Table in self.Keys.get(aTable, []):
                if (Table in ResSort):
                    Res = max(Res, ResSort.index(Table))
            if (Res):
                Res += 1
            return Res

        def GetTables():
            Res = set()
            for Key, Val in self.Keys.items():
                Res.add(Key)
                Res.update(Val)
            return Res

        Tables = GetTables()
        for Table in Tables:
            if Table == 'ref_tenant':
                print(Table)
            Pos = SearchLastPos(Table)
            ResSort.insert(Pos, Table)

        return ResSort

    def Create(self):
        Name = 'ref_product'
        _, Data = self._FindTable(Name)
        Res = TPgMeta.AddTableMeta(Name, Data)
        print(Res)


    def LoadModel(self, aName: str):
        Tables = DeepGet(self.Data, f'{aName}.table', {})
        for Table in Tables:
            self._LoadTable(Table)
