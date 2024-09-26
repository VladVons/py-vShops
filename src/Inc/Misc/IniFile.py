# Created: 2024.09.23
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
from Inc.Var.Dict import DeepGet, DeepSetByList


class TIniFile():
    def __init__(self):
        self.Data = {}

    def Read(self, aFile: str):
        Sect = ''
        reSect = re.compile(r'\[\s*(.*?)\s*\]')

        with open(aFile, 'r', encoding = 'utf8') as F:
            Lines = F.readlines()

        for Line in Lines:
            Line = Line.strip('')
            if (Line):
                if ('=' in Line):
                    Key, Val = Line.split('=')
                    self.SetSectionVal(Sect, Key, Val)
                elif (Line.startswith('[')):
                    Match = reSect.search(Line)
                    if (Match):
                        Sect = Match.group(1)
                        self.AddSection(Sect)

    def AddSection(self, aSect: str):
        self.Data[aSect] = {}

    def GetData(self, aPath: str) -> dict:
        if (aPath):
            assert(aPath.count('.') <= 1), 'Path too long'
            Res = DeepGet(self.Data, aPath)
        else:
            Res = self.Data
        return Res

    def GetSections(self) -> list[str]:
        return [xKey for xKey, xVal in self.Data.items() if isinstance(xVal, dict)]

    def SetSectionVal(self, aSect: str, aKey: str, aVal):
        DeepSetByList(self.Data, [aSect.strip(), aKey.strip()], str(aVal).strip())
