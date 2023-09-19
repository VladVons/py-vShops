# Created: 2022.05.25
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import sqlite3
#
from Inc.DbList import TDbSql
from .Common import TEngine


class TParser_sqlite(TEngine):
    _Sheet: TDbSql

    def _InitEngine(self, aFile: str):
        return sqlite3.connect(aFile)

    def SetSheet(self, aQuery: str):
        Cur = self._Engine.cursor()
        Cur.execute(aQuery)
        Fields = [x[0]for x in Cur.description]
        Data = Cur.fetchall()
        self._Sheet = TDbSql(Fields, Data)

    async def _Load(self):
        assert(self._Sheet), 'SetSheet() first'

        for RowNo, Rec in enumerate(self._Sheet):
            Data = {'no': RowNo} | Rec.GetAsDict()
            self._Fill(Data)
            await self.Sleep.Update()

    def _Fill(self, aRow: dict):
        raise NotImplementedError()
