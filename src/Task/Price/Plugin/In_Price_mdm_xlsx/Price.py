# Created: 2023.01.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
#
from Inc.DbList import TDbRec
from Inc.Util.Str import ToFloat, ToHashWM
from Inc.Util.Obj import GetNotNone
from Inc.ParserX.Parser_xlsx import TParser_xlsx
from ..CommonDb import TDbCompPC, TDbCompMonit, GetTitle


class TFiller():
    def __init__(self, aParent):
        self.Parent = aParent

        Conf = aParent.GetConfSheet()
        self.ConfTitle = Conf.get('title', [])
        self.ConfModel = Conf.get('model', ['model'])

    def Add(self, aRow: dict, aRec: TDbRec, aFieldsCopy: list):
        for x in aFieldsCopy:
            self.Parent.Copy(x, aRow, aRec)

        Arr = [str(aRow.get(x, '')) for x in self.ConfModel]
        Model = ToHashWM(' '.join(Arr))
        aRec.SetField('code', Model)

        Title = GetTitle(aRow, self.ConfTitle, '/')
        Title = Title.replace('"', '').lower()
        aRec.SetField('title', Title)

        Val = ToFloat(aRow.get('price'))
        aRec.SetField('price', Val)


class TPricePC(TParser_xlsx):
    def __init__(self, aParent):
        super().__init__(aParent, TDbCompPC())
        self.Filler: TFiller

        self.ReDisk = re.compile(r'(\d+)\s*(hdd|ssd)', re.IGNORECASE)
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
            Rec.SetField('disk', Data[1])

            Val = f'{Data[0]} {Data[1]}'
            aRow['disk'] = Val

        Val = aRow.get('ram', '')
        Data = self.ReRam.findall(Val)
        if (Data):
            Data = Data[0]
            Rec.SetField('ram_size', int(Data[0]))

            Val = f'{Data[0]}{Data[1].capitalize()}'
            aRow['ram'] = Val

        self.Filler.Add(aRow, Rec, ['cpu', 'case', 'os', 'grade'])

        Rec.Flush()


class TPriceMonit(TParser_xlsx):
    def __init__(self, aParent):
        super().__init__(aParent, TDbCompMonit())
        self.Filler: TFiller

    def _OnLoad(self):
        self.Filler = TFiller(self)

    def _Filter(self, aRow: dict):
        return (not aRow.get('price'))

    def _Fill(self, aRow: dict):
        if (self._Filter(aRow)):
            return

        Rec = self.Dbl.RecAdd()

        Val = GetNotNone(aRow, 'screen', '').replace('"', '')
        Rec.SetField('screen', Val)

        aRow['model'] = aRow['model'].rstrip('-')

        self.Filler.Add(aRow, Rec, ['grade'])

        Rec.Flush()


class TPriceNotebook(TPricePC):
    def _Filter(self, aRow: dict):
        return (not aRow.get('price'))

    def _Fill(self, aRow: dict):
        Val = aRow.get('category')
        Data = re.findall(r'(\d+)', Val)
        if (Data):
            aRow['screen'] = Data[0]
        else:
            aRow['screen'] = ''

        super()._Fill(aRow)
