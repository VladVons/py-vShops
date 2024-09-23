# Created: 2023.11.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
#
from Inc.DbList import TDbRec
from Inc.Util.Str import ToFloat, ToHashWM, Replace
from Inc.Util.Dict import GetNotNone
from Inc.ParserX.Parser_xlsx import TParser_xlsx
from ..CommonDb import TDbCompPC, TDbCompMonit, TDbPrinter, TScheme


ReplaceWin = {
    'W7P': 'Windows 7 Pro',
    'W8P': 'Windows 8 Pro',
    'W10P': 'Windows 10 Pro',
    'W11P': 'Windows 11 Pro',
}


class TFiller():
    def __init__(self, aParent):
        self.Parent = aParent
        Conf = aParent.GetConfSheet()
        self.ConfTitle = Conf.get('title', [])
        self.ConfModel = Conf.get('model', ['model'])
        self.ConfAttr = Conf.get('attr', {})

    def SetBase(self, aRow: dict, aRec: TDbRec, aFieldsCopy: list):
        Val = aRow.get('model').upper()
        aRow['model'] = Val

        Val = self.Parent.Parent.Conf.get('cond', 'used')
        aRec.SetField('cond', Val)

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

        Scheme = TScheme()
        Attr = Scheme.ParsePipes(aRow, self.ConfAttr)
        aRec.SetField('attr', Attr)


class TPricePC(TParser_xlsx):
    def __init__(self, aParent):
        super().__init__(aParent, TDbCompPC())
        self.Filler: TFiller

        self.ReDisk1 = re.compile(r'(\d+)\s*(gb|tb)\s*(hdd|ssd)', re.IGNORECASE)
        self.ReDisk2 = re.compile(r'(\d+)\s*(hdd|ssd)', re.IGNORECASE)
        self.ReDisk3 = re.compile(r'(\d+)x(\d+)\s*(gb|tb)\s*(hdd|ssd)', re.IGNORECASE)
        self.ReRam = re.compile(r'(\d+)\s*(gb)', re.IGNORECASE)

    def _OnLoad(self):
        self.Filler = TFiller(self)

    def _Fill(self, aRow: dict) -> TDbRec:
        if (not aRow.get('price')):
            return

        Rec = self.Dbl.RecAdd()

        Val = aRow.get('disk', '')
        if (Val):
            # 4x256GB SSD
            Data = self.ReDisk3.findall(Val)
            if (Data):
                Data = Data[0]
                Size = int(Data[0]) * int(Data[1])
                Rec.SetField('disk_size', Size)
                Rec.SetField('disk', Data[3])
                aRow['disk'] = f'{Size}{Data[2]} {Data[3]}'
            else:
                # 256GB SSD, 256GBSSD
                Data = self.ReDisk1.findall(Val)
                if (Data):
                    Size = 0
                    for xData in Data:
                        Size += int(xData[0])
                    Data = Data[0]
                    Rec.SetField('disk_size', Size)
                    Rec.SetField('disk', Data[2])
                    aRow['disk'] = f'{Size}{Data[1]} {Data[2]}'
                else:
                    # 256SSD
                    Data = self.ReDisk2.findall(Val)
                    if (Data):
                        Data = Data[0]
                        Rec.SetField('disk_size', int(Data[0]))
                        Rec.SetField('disk', Data[1])
                        aRow['disk'] = f'{Data[0]}GB {Data[1]}'
        else:
            Rec.SetField('disk_size', 0)

        Val = str(aRow.get('ram', ''))
        # 4Gb, 4 Gb
        Data = self.ReRam.findall(Val)
        if (Data):
            Data = Data[0]
            Rec.SetField('ram_size', int(Data[0]))
            aRow['ram'] = f'{Data[0]}{Data[1]}'
        else:
            # 4
            Rec.SetField('ram_size', int(Val))
            aRow['ram'] = f'{Val}GB'

        aRow['os'] = Replace(aRow['os'], ReplaceWin)

        self.Filler.SetBase(aRow, Rec, ['cpu', 'case', 'vga', 'os', 'qty'])
        return Rec

class TPriceMonit(TParser_xlsx):
    def __init__(self, aParent):
        super().__init__(aParent, TDbCompMonit())
        self.Filler: TFiller

    def _OnLoad(self):
        self.Filler = TFiller(self)

    def _Filter(self, aRow: dict):
        return (not aRow.get('price')) or (aRow.get('stand', '').lower() != 'yes')

    def _Fill(self, aRow: dict) -> TDbRec:
        if (self._Filter(aRow)):
            return

        Rec = self.Dbl.RecAdd()

        Val = GetNotNone(aRow, 'grade', '').replace('-', '')
        Rec.SetField('grade', Val)
        aRow['grade'] = Val

        Val = GetNotNone(aRow, 'screen', '').replace('"', '')
        Rec.SetField('screen', Val)
        aRow['screen'] = f'{Val}"'

        self.Filler.SetBase(aRow, Rec, ['color', 'qty'])
        return Rec


class TPriceLaptop(TPricePC):
    def _Filter(self, aRow: dict):
        return (not aRow.get('price'))

    def _Fill(self, aRow: dict) -> TDbRec:
        Rec = super()._Fill(aRow)
        if (not Rec):
            return

        Val = GetNotNone(aRow, 'screen', '').replace('"', '')
        aRow['screen'] = f'{Val}"'


class TPricePrinter(TParser_xlsx):
    def __init__(self, aParent):
        super().__init__(aParent, TDbPrinter())
        self.Filler: TFiller

    def _OnLoad(self):
        self.Filler = TFiller(self)

    def _Fill(self, aRow: dict) -> TDbRec:
        if (not aRow.get('price')):
            return

        Rec = self.Dbl.RecAdd()
        self.Filler.SetBase(aRow, Rec, ['qty'])
        return Rec
