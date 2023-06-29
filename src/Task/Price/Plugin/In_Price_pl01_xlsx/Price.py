# Created: 2023.01.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
#
from Inc.DbList import TDbRec
from Inc.Util.Str import ToFloat, ToHashWM
from Inc.Util.Obj import GetNotNone
from Inc.ParserX.Parser_xlsx import TParser_xlsx
from ..CommonDb import TDbCompPC, TDbCompMonit


class TFiller():
    def __init__(self, aParent):
        self.Parent = aParent

        Conf = aParent.GetConfSheet()
        self.ConfTitle = Conf.get('title', [])
        self.ConfModel = Conf.get('model', ['model'])

    def Add(self, aRow: dict, aFieldsCopy: list) -> TDbRec:
        Rec = self.Parent.Dbl.RecAdd()

        for x in aFieldsCopy:
            self.Parent.Copy(x, aRow, Rec)

        Arr = [str(aRow.get(x, '')) for x in self.ConfModel]
        Model = ToHashWM(' '.join(Arr))
        Rec.SetField('code', Model)

        Arr = [str(aRow[x]) for x in self.ConfTitle]
        Title = '/'.join(Arr).replace('"', '')
        Rec.SetField('title', Title)

        Val = ToFloat(aRow.get('price'))
        Rec.SetField('price', Val)

        return Rec


class TPricePC(TParser_xlsx):
    def __init__(self, aParent):
        super().__init__(aParent, TDbCompPC())
        self.Filler: TFiller

        self.ReDisk = re.compile(r'(\d+)\s*(gb|tb)\s*(hdd|ssd)', re.IGNORECASE)
        self.ReRam = re.compile(r'(\d+)\s*(gb)', re.IGNORECASE)

    def _OnLoad(self):
        self.Filler = TFiller(self)

    def _Fill(self, aRow: dict):
        if (not aRow.get('price')):
            return

        Rec = self.Filler.Add(aRow, ['cpu', 'case', 'dvd', 'vga', 'os'])

        Val = aRow.get('disk', '')
        Data = self.ReDisk.findall(Val)
        if (Data):
            Data = Data[0]
            Rec.SetField('disk_size', int(Data[0]))
            Rec.SetField('disk', Data[2])

        Val = aRow.get('ram', '')
        Data = self.ReRam.findall(Val)
        if (Data):
            Data = Data[0]
            Rec.SetField('ram_size', int(Data[0]))

        Rec.Flush()


class TPriceMonit(TParser_xlsx):
    def __init__(self, aParent):
        super().__init__(aParent, TDbCompMonit())
        self.Filler: TFiller

    def _OnLoad(self):
        self.Filler = TFiller(self)

    def _Filter(self, aRow: dict):
        return (not aRow.get('price')) or (aRow.get('stand', '').lower() != 'yes')

    def _Fill(self, aRow: dict):
        if (self._Filter(aRow)):
            return

        Rec = self.Filler.Add(aRow, ['grade', 'color'])

        Val = GetNotNone(aRow, 'screen', '').replace('"', '')
        Rec.SetField('screen', Val)

        Rec.Flush()


class TPriceMonitInd(TPriceMonit):
    def _Filter(self, aRow: dict):
        return (not aRow.get('price'))
