# Created: 2022.03.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import operator


class TDbCond(list):
    # aCond is [ (operator.lt, Db1.Fields.GetNo('age'), 40, True), (...) ]
    def Add(self, aOp: operator, aFieldNo: int, aVal, aRes: bool):
        self.append([aOp, aFieldNo, aVal, aRes])

    def AddField(self, aOp: str, aField: tuple, aVal, aRes: bool):
        Dbl, Name = aField
        Func = getattr(operator, aOp, None)
        self.Add(Func, Dbl.Fields.GetNo(Name), aVal, aRes)

    def AddFields(self, aConds: list):
        for Row in aConds:
            self.AddField(*Row)
        return self

    def Find(self, aData: list) -> bool:
        for Func, FieldNo, Val, CmpRes in self:
            if (not Func(aData[FieldNo], Val) == CmpRes):
                return False
        return True
