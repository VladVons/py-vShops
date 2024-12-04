# Created: 2024.12.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re

class TSpecBase():
    def __init__(self):
        self.Patterns = self._Compile()

    def _GetPatterns(self) -> dict:
        raise NotImplementedError()

    def _OnParse(self, aRes: dict, aKey: str, aMatch):
        Data = [xMatch.lower() for xMatch in aMatch.groups() if xMatch]
        aRes[aKey] = Data

    def _Compile(self) -> dict:
        Res = {}
        Patterns = self._GetPatterns()
        for xKey, xVal in Patterns.items():
            if (not xKey.startswith('-')):
                if (isinstance(xVal, list)):
                    Obj = [
                        re.compile(xPattern, re.IGNORECASE)
                        for xPattern in xVal
                    ]
                else:
                    Obj = xVal
                Res[xKey] = Obj
        return Res

    def Parse(self, aText: str) -> list:
        Res = {}
        if (aText):
            for _Idx, (xKey, xVal) in enumerate(self.Patterns.items()):
                if (isinstance(xVal, list)):
                    for xPattern in xVal:
                        Match = xPattern.search(aText)
                        if (Match):
                            self._OnParse(Res, xKey, Match)
                            break
                else:
                    R = xVal.Parse(aText)
                    if (R):
                        Res[xKey] = R
        return Res
