# Created: 2023.01.20
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Obj import DeepSetByList, DeepGet
from Inc.DbList import TDbSql
from .ADb import TDbExecCurs
from .DbPg import TDbPg


class TDbMeta():
    def __init__(self, aDb: TDbPg):
        self.Db = aDb
        self.Foreign = TForeign(self)
        self.Table = TTable(self)

    async def Init(self):
        await self.Foreign.Init()
        await self.Table.Init()

    async def Delete(self, aTable: str, aWhere: str, aCursor = None) -> TDbSql:
        Where = f'where {aWhere}' if aWhere else ''

        Query = f'''
            delete from {aTable}
            {Where}
        '''
        return await TDbExecCurs(aCursor).Exec(Query)

class TMeta():
    def __init__(self, aParent: TDbMeta):
        self.Parent = aParent

class TForeign(TMeta):
    def __init__(self, aParent: TDbMeta):
        super().__init__(aParent)
        self.TableColumn = {}
        self.TableId = {}

    async def Init(self):
        self.TableColumn = {}
        self.TableId = {}

        Dbl = await self.Parent.Db.GetForeignKeys()
        for Rec in Dbl:
            Table = Rec.GetField('table_name')
            Column = Rec.GetField('column_name')
            TableF = Rec.GetField('table_name_f')
            ColumnF = Rec.GetField('column_name_f')

            Key = (Table, Column)
            self.TableColumn[Key] = (TableF, ColumnF)

            Key = (TableF, ColumnF)
            self.TableId[Key] = self.TableId.get(Key, {}) | {Table: Column}

    def GetColumnVal(self, aTable: str, aTableId: tuple):
        Res = {}
        if (aTableId):
            Column = self.TableId[(aTableId[0], 'id')].get(aTable)
            if (Column):
                Res[Column] = aTableId[1]
        return Res



class TTable(TMeta):
    def __init__(self, aParent: TDbMeta):
        super().__init__(aParent)
        self.Column = {}
        self.Require = {}

    async def Init(self):
        self.Column = {}
        self.Require = {}

        Dbl = await self.Parent.Db.GetTableColumns()
        for Rec in Dbl:
            Table = Rec.GetField('table_name')
            Column = Rec.GetField('column_name')
            Key = (Table, Column)
            Value = {'type': Rec.column_type, 'null': Rec.is_null.lower()}
            DeepSetByList(self.Column, Key, Value)

            if (Value['null'] == 'no') and (Column != 'id'):
                if (Table not in self.Require):
                    self.Require[Table] = []
                self.Require[Table] += [Column]

    def Get(self, aPath: str) -> object:
        return DeepGet(self.Column, aPath)
