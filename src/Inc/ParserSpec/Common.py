# Created: 2024.12.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import re

class TSpecBase():
    def __init__(self):
        self.Patterns = self._GetPatternsObj()

    def _GetPatterns(self) -> dict:
        raise NotImplementedError()

    def _GetPatternsObj(self) -> dict:
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
        for _Idx, (xKey, xVal) in enumerate(self.Patterns.items()):
            if (isinstance(xVal, list)):
                for xPattern in xVal:
                    Match = xPattern.search(aText)
                    if (Match):
                        q1 = Match.groups()
                        R = [xMatch.lower() for xMatch in Match.groups() if xMatch]
                        Res[xKey] = R
                        break
            else:
                R = xVal.Parse(aText)
                if (R):
                    Res[xKey] = R
        return Res
