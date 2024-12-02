# Created: 2024.12.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import re

class TSpecBase():
    def __init__(self):
        self.Patterns = [
            re.compile(xPattern, re.IGNORECASE)
            for xPattern in self._GetPatterns()
        ]

    def _GetPatterns(self) -> list:
        raise NotImplementedError()

    def Parse(self, aText: str) -> list:
        for _Idx, xPattern in enumerate(self.Patterns):
            Match = xPattern.search(aText)
            if (Match):
                Res = [xMatch.lower() for xMatch in Match.groups() if xMatch]
                return Res
