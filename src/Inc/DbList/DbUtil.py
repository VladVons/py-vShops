# Created: 2024.08.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from io import BytesIO
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font
#
from .DbList import TDbList


def DblToXlsx(aDbl: list[TDbList]) -> bytes:
    WB = Workbook()
    WB.remove(WB.active)
    for Idx, xDbl in enumerate(aDbl):
        Title = xDbl.Tag if xDbl.Tag else f'Sheet{Idx+1}'
        WS = WB.create_sheet(title=Title)

        RowNo = 1
        Fields = xDbl.GetFields()
        Rec = xDbl.RecGo(0)
        for Idx, Field in enumerate(Fields):
            Cell = WS.cell(RowNo, Idx + 1)
            Cell.value = Field
            Cell.font = Font(bold = True)

            CD = WS.column_dimensions[get_column_letter(Idx + 1)]
            Val = Rec.GetField(Field)
            if (isinstance(Val, int)):
                CD.number_format = '#0'
            elif (isinstance(Val, float)):
                CD.number_format = '#,##0.00'

        RowNo += 1
        WS.freeze_panes = WS.cell(RowNo, 1)
        for Rec in xDbl:
            for Idx, Field in enumerate(Fields):
                Cell = WS.cell(RowNo + xDbl.RecNo, Idx + 1).value = Rec.GetField(Field)

    Stream = BytesIO()
    WB.save(Stream)
    Res = Stream.getvalue()
    Stream.close()
    return Res
