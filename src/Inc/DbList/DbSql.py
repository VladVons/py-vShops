# Created: 2023.02.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from .DbList import TDbList


class TDbSql(TDbList):
    def GetSqlInsert(self, aTable: str, aReturning: list[str] = None) -> str:
        if (self.GetSize() > 0):
            Fields = self.GetFields()
            Fields = '(%s)' % (', '.join(Fields))
            Values = [Rec.GetAsSql() for Rec in self]
            Values = 'values(%s)' % ('), ('.join(Values))
        else:
            Fields = ''
            Values = 'default values'

        Returning = 'returning ' + ', '.join(aReturning) if aReturning else ''
        return f'''
            insert into {aTable}
            {Fields}
            {Values}
            {Returning}
        '''

    def GetSqlUpdate(self, aTable: str, aRecNo: int = 0) -> str:
        self.RecNo = aRecNo
        return 'update %s set %s' % (aTable, self.Rec.GetAsSql())

    def GetSqlInsertUpdate(self, aTable: str, aUniqField: str) -> str:
        Insert = self.GetSqlInsert(aTable)
        Set = [
            '%s = excluded.%s' % (Key, Key)
            for Key in self.GetFields()
            if (Key != aUniqField)
        ]
        Set = ', '.join(Set)

        return f'''
            {Insert}
            on conflict ({aUniqField}) do update
            set {Set}
            returning id;
        '''

    def ExportListComma(self, aField: str) -> str:
        FieldNo = self.GetFieldNo(aField)
        if (isinstance(self.Data[0][FieldNo], str)):
            Res = [x[FieldNo] for x in self.Data]
            Res = "'" + "', '".join(Res) + "'"
        else:
            Res = [str(x[FieldNo]) for x in self.Data]
            Res = ', '.join(Res)
        return Res
