# Created: 2024.12.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from Inc import ParserSpec


class TSpecComp():
    def __init__(self):
        self.Parsers = {
            'category': ParserSpec.TSpecCategory(),
            'brand': ParserSpec.TSpecBrand(),
            'case': ParserSpec.TSpecCase(),
            'cpu': ParserSpec.TSpecCpu(),
            'ram': ParserSpec.TSpecRam(),
            'disk': ParserSpec.TSpecStorage(),
            'screen': ParserSpec.TSpecScreen(),
            'os': ParserSpec.TSpecOs()
        }

    def Parse(self, aText: str) -> dict:
        Res = {}
        for xKey, xParser in self.Parsers.items():
            if (not xKey.startswith('-')):
                R = xParser.Parse(aText)
                if (R):
                    Res.update(R)
        return Res

def TestAll(aFile: str):
    with open(aFile, 'r', encoding='utf8') as F:
        Lines = []
        for xLine in F.readlines():
            xLine = xLine.strip()
            if (xLine) and (not xLine.startswith('-')):
                Lines.append(xLine)

    SpecComp = TSpecComp()
    for Idx, xLine in enumerate(Lines):
        print(f'{Idx+1}/{len(Lines)}: {xLine}')
        Spec = SpecComp.Parse(xLine)
        for xKey, xVal in Spec.items():
            print(xKey, ':', xVal)
        print()
