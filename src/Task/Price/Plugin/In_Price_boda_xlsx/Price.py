# Created: 2023.11.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
#
from Inc.DbList import TDbRec
from Inc.Util.Str import ToFloat, ToHashWM
from Inc.Util.Obj import GetNotNone
from Inc.ParserX.Parser_xlsx import TParser_xlsx
from ..CommonDb import TDbCompPC, TDbCompMonit, TDbPrinter


class TFiller():
    def __init__(self, aParent):
        self.Parent = aParent
        Conf = aParent.GetConfSheet()
        self.ConfTitle = Conf.get('title', [])
        self.ConfModel = Conf.get('model', ['model'])

    def SetBase(self, aRow: dict, aRec: TDbRec, aFieldsCopy: list):
        Val = aRow.get('model').upper()
        aRow['model'] = Val

        Val = self.Parent.Parent.Conf.get('used', False)
        aRec.SetField('used', Val)

        for x in aFieldsCopy:
            self.Parent.Copy(x, aRow, aRec)

        Arr = [str(aRow.get(x, '')) for x in self.ConfModel if aRow[x]]
        Model = ToHashWM(' '.join(Arr))
        aRec.SetField('code', Model)

        Arr = [str(aRow[x]).strip() for x in self.ConfTitle if aRow[x]]
        Title = '/'.join(Arr).replace('"', '')
        aRec.SetField('title', Title)

        for x in ['price', 'price_in']:
            Val = ToFloat(aRow.get(x))
            aRec.SetField(x, Val)


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

        Rec = self.Dbl.RecAdd()

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

        #self.Filler.SetBase(aRow, Rec, ['cpu', 'case', 'dvd', 'vga', 'os'])
        self.Filler.SetBase(aRow, Rec, ['cpu', 'case', 'vga', 'os', 'qty'])

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

        Rec = self.Dbl.RecAdd()

        Val = GetNotNone(aRow, 'grade', '').replace('-', '')
        Rec.SetField('grade', Val)
        aRow['grade'] = Val

        Val = GetNotNone(aRow, 'screen', '').replace('"', '')
        Rec.SetField('screen', Val)

        self.Filler.SetBase(aRow, Rec, ['color', 'qty'])

        Rec.Flush()


class TPriceLaptop(TPricePC):
    def _Filter(self, aRow: dict):
        return (not aRow.get('price'))


class TPricePrinter(TParser_xlsx):
    def __init__(self, aParent):
        super().__init__(aParent, TDbPrinter())
        self.Filler: TFiller

    def _OnLoad(self):
        self.Filler = TFiller(self)

    def _Fill(self, aRow: dict):
        if (not aRow.get('price')):
            return

        Rec = self.Dbl.RecAdd()
        self.Filler.SetBase(aRow, Rec, ['qty'])
        Rec.Flush()
