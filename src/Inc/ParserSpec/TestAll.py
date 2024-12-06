# Created: 2024.12.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from Inc.ParserSpec import (
    TSpecCategory, TSpecBrand, TSpecCase, TSpecCpu, TSpecRam, TSpecStorage, TSpecScreenResol, TSpecScreenSize, TSpecOs
)


class TSpecComp():
    def __init__(self):
        self.Parsers = {
            'category': TSpecCategory(),
            'brand': TSpecBrand(),
            'case': TSpecCase(),
            'cpu': TSpecCpu(),
            'ram': TSpecRam(),
            'storage': TSpecStorage(),
            'screen_size': TSpecScreenSize(),
            'screen_resol': TSpecScreenResol(),
            'os': TSpecOs()
        }

    def Parse(self, aText: str) -> dict:
        Res = {}
        for xKey, xParser in self.Parsers.items():
            if (not xKey.startswith('-')):
                R = xParser.Parse(aText)
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
            if (xLine) and (not xLine.startswith('-')):
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
