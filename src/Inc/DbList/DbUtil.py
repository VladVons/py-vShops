# Created: 2024.08.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from io import BytesIO
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font
#
from .DbList import TDbList


def DblToXlsx(aDbl: TDbList) -> bytes:
    WB = Workbook()
    WS = WB.active
    WS.title = "price"

    RowNo = 1
    Fields = aDbl.GetFields()
    Rec = aDbl.RecGo(0)
    for Idx, Field in enumerate(Fields):
        CD = WS.column_dimensions[get_column_letter(Idx + 1)]

        Cell = WS.cell(RowNo, Idx + 1)
        Cell.value = Field
        Cell.font = Font(bold = True)
        if (isinstance(Rec.GetField(Field), (int, float))):
            CD.number_format = '#,##0.00'

    RowNo += 1
    WS.freeze_panes = WS.cell(RowNo, 1)
    for Rec in aDbl:
        for Idx, Field in enumerate(Fields):
            Cell = WS.cell(RowNo + aDbl.RecNo, Idx + 1).value = Rec.GetField(Field)

    Stream = BytesIO()
    WB.save(Stream)
    Res = Stream.getvalue()
    Stream.close()
    return Res
