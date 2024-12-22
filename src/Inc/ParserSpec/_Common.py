# Created: 2024.12.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re


def ToGbUnit(aVal: int, aName: str = 'gb') -> tuple:
    Table = {
        'tb': 1000,
        'gb': 1,
        'mb': 0.001
    }

    Val = Table.get(aName)
    if (Val):
        aVal *= Val
        aName = 'gb'
    return (aVal, aName)

class TLang():
    def __init__(self):
        self.Data = {
            'гб': 'gb',
            'тб': 'tb',
        }

    def Translate(self, aVal: str) -> str:
        Val = aVal.lower()
        return self.Data.get(Val, Val)


class TSpecBase():
    def __init__(self, aReOpt = None):
        if (not aReOpt):
            self.ReOpt = re.IGNORECASE
        self.Patterns = self._Compile()

    def _GetPatterns(self) -> dict:
        raise NotImplementedError()

    def _OnParse(self, aRes: dict, aKey: str, aMatch) -> bool:
        Data = [xMatch.lower() for xMatch in aMatch.groups() if xMatch]
        aRes[aKey] = Data
        return False

    def _Compile(self) -> dict:
        Res = {}
        Patterns = self._GetPatterns()
        for xKey, xVal in Patterns.items():
            if (not xKey.startswith('-')):
                if (isinstance(xVal, list)):
                    xVal = [re.compile(xPattern, self.ReOpt) for xPattern in xVal]
                Res[xKey] = xVal
        return Res

    def Parse(self, aText: str) -> dict:
        Res = {}
        if (aText):
            for _Idx, (xKey, xVal) in enumerate(self.Patterns.items()):
                if (isinstance(xVal, list)):
                    for xPattern in xVal:
                        Match = xPattern.search(aText)
                        if (Match):
                            Quit = self._OnParse(Res, xKey, Match)
                            if (Quit is True):
                                return Res
                            break
                else:
                    R = xVal.Parse(aText)
                    if (R):
                        Res[xKey] = R
        return Res


Lang = TLang()
