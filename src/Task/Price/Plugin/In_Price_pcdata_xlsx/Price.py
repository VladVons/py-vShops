# Created: 2023.01.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
#
from Inc.DbList import TDbRec
from Inc.Var.Str import ToFloat, ToHashWM
from Inc.Var.Dict import GetNotNone
from Inc.ParserX.Parser_xlsx import TParser_xlsx
from ..CommonDb import TDbCompPC, TDbCompMonit, TDbPrinter, GetTitleValues, TScheme


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
            if (aRow.get(x) == '--'):
                aRow[x] = ''
            self.Parent.Copy(x, aRow, aRec)

        #Arr = [str(aRow.get(x, '')) for x in self.ConfModel]
        Arr = GetTitleValues(aRow, self.ConfModel)
        Model = ToHashWM(' '.join(Arr))
        aRec.SetField('code', Model)

        #Arr = [str(aRow[x]).strip() for x in self.ConfTitle]
        Arr = GetTitleValues(aRow, self.ConfTitle)
        #Title = '/'.join(Arr).replace('"', '')
        Title = ' '.join(Arr).replace('"', '')
        aRec.SetField('title', Title)

        for x in ['price', 'price_in']:
            Val = ToFloat(aRow.get(x))
            aRec.SetField(x, Val)

        Scheme = TScheme()
        Attr = Scheme.ParsePipes(aRow, self.ConfAttr)
        for Key, Val in Attr.items():
            if (len(Val) >= 32):
                Attr[Key] = ''
        aRec.SetField('attr', Attr)

class TPricePC(TParser_xlsx):
    def __init__(self, aParent):
        super().__init__(aParent, TDbCompPC())
        self.Filler: TFiller

        self.ReDisk = re.compile(r'(\d+)\s*(gb|tb)\s*(hdd|ssd)', re.IGNORECASE)
        self.ReRam = re.compile(r'(\d+)\s*(gb)', re.IGNORECASE)

    def _OnLoad(self):
        self.Filler = TFiller(self)

    def _Filter(self, aRow: dict):
        return (not aRow.get('price_in')) or (not aRow.get('ram')) or (not aRow.get('disk')) or ('--' in aRow.get('disk'))

    def _Fill(self, aRow: dict) -> TDbRec:
        if (self._Filter(aRow)):
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

        # MaxLen = len('Windows 10 Home')
        MaxLen = 17
        Val = aRow.get('os', '')
        if Val and (len(Val) > MaxLen):
            Rec.SetField('os', Val[:MaxLen])

        self.Filler.SetBase(aRow, Rec, ['cpu', 'case', 'vga', 'os'])
        return Rec

class TPriceNotebook(TPricePC):
    def _Fill(self, aRow: dict):
        Val = aRow.get('screen', '')
        if (Val):
            Data = re.findall(r'(\d+)', Val)
            if (Data):
                aRow['screen'] = Data[0]
            else:
                aRow['screen'] = ''

        super()._Fill(aRow)

class TPriceMonit(TParser_xlsx):
    def __init__(self, aParent):
        super().__init__(aParent, TDbCompMonit())
        self.Filler: TFiller

    def _OnLoad(self):
        self.Filler = TFiller(self)

    def _Filter(self, aRow: dict):
        return (not aRow.get('price_in')) or (aRow.get('stand', '').lower() != 'yes')

    def _Fill(self, aRow: dict) -> TDbRec:
        if (self._Filter(aRow)):
            return

        Rec = self.Dbl.RecAdd()

        Val = GetNotNone(aRow, 'grade', '').replace('-', '')
        if (not Val):
            Val = 'A'
        Rec.SetField('grade', Val)
        aRow['grade'] = Val

        Val = GetNotNone(aRow, 'screen', '').replace('"', '')
        Rec.SetField('screen', Val)

        self.Filler.SetBase(aRow, Rec, ['color'])
        return Rec


class TPriceMonitInd(TPriceMonit):
    def _Filter(self, aRow: dict):
        return (not aRow.get('price_in'))


class TPricePrinter(TParser_xlsx):
    def __init__(self, aParent):
        super().__init__(aParent, TDbPrinter())
        self.Filler: TFiller

    def _OnLoad(self):
        self.Filler = TFiller(self)

    def _Fill(self, aRow: dict) -> TDbRec:
        if (not aRow.get('price_in')):
            return

        Rec = self.Dbl.RecAdd()
        self.Filler.SetBase(aRow, Rec, ['qty'])
        return Rec
