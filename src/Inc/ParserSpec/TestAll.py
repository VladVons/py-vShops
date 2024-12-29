# Created: 2024.12.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from Inc.ParserSpec import (
    TSpecCategory, TSpecBrand, TSpecCaseComputer, TSpecCpu, TSpecRam, TSpecStorage, TSpecScreenResol,
    TSpecScreenSize, TSpecOs, TSpecGrade
)


class TSpecComp():
    def __init__(self):
        self.Parsers = {
            'category': TSpecCategory(),
            'brand': TSpecBrand(),
            'grade': TSpecGrade(),
            'case_computer': TSpecCaseComputer(),
            'cpu': TSpecCpu(),
            'ram': TSpecRam(),
            'storage': TSpecStorage(),
            'screen_size': TSpecScreenSize(),
            'screen_resol': TSpecScreenResol(),
            'os': TSpecOs()
        }

        self.Base = ['brand', 'grade']

        self.Categories = {
            'desktop':     self.Base + ['case_computer', 'cpu', 'ram', 'storage', 'os'],
            'server':      self.Base + ['case_computer', 'cpu', 'ram', 'storage', 'os'],
            'thin client': self.Base + ['case_computer', 'cpu', 'ram', 'storage', 'os'],

            'laptop': self.Base + ['cpu', 'ram', 'storage', 'os', 'screen_size', 'screen_resol'],
            'aio':    self.Base + ['cpu', 'ram', 'storage', 'os', 'screen_size', 'screen_resol'],
            'pos':    self.Base + ['cpu', 'ram', 'storage', 'os', 'screen_size', 'screen_resol'],

            'storage': self.Base + ['storage'],

            'monitor': self.Base + ['screen_size', 'screen_resol'],

            'mobile': self.Base + ['cpu', 'ram', 'storage', 'screen_size', 'screen_resol'],
        }

    def Parse(self, aText: str) -> dict:
        Res = self.Parsers['category'].Parse(aText)
        if (Res):
            Name = Res.get('category')
            Parsers = self.Categories.get(Name, self.Base)
            for xParser in Parsers:
                if (not xParser.startswith('-')):
                    R = self.Parsers[xParser].Parse(aText)
                    if (R):
                        Res.update(R)
        return Res

    @staticmethod
    def ParseLines(aLines: list) -> list:
        Res = []
        SpecComp = TSpecComp()
        for Idx, xLine in enumerate(aLines):
            Res.append(f'{Idx+1}/{len(aLines)}: {xLine}')
            Spec = SpecComp.Parse(xLine)
            for xKey, xVal in Spec.items():
                Res.append(f'{xKey}: {xVal}')
            Res.append('')
        return Res

    @staticmethod
    def GetLines(aText: str) -> list[str]:
        Lines = []
        for xLine in aText.splitlines():
            xLine = xLine.strip()
            if (xLine):
                if (xLine.startswith('-')):
                    if (xLine == '-!'):
                        break
                else:
                    Lines.append(xLine)
        return Lines

    @staticmethod
    def ParseFile(aFile: str):
        with open(aFile, 'r', encoding='utf8') as F:
            Data = F.read()
            Lines = TSpecComp.GetLines(Data)

        Lines = TSpecComp.ParseLines(Lines)
        for xLine in Lines:
            print(xLine)
