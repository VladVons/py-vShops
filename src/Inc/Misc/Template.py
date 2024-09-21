# Created: 2023.03.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re


class TDictRepl():
    def __init__(self, aDict: dict = None):
        self.Dict = aDict or {}
        self.UserData = None
        self._VarTpl()

    def _VarTpl(self):
        #self.ReVar = re.compile(r'(\$\w+)\b')
        self.ReVar = re.compile(r'(\$[a-zA-Z0-9]+)')

    def _Get(self, aFind: str) -> str:
        return self.Dict.get(aFind, f'-{aFind}-')

    def Parse(self, aStr: str) -> str:
        if (aStr) :
            while (True):
                Arr = self.ReVar.search(aStr)
                if (not Arr):
                    break
                Find = Arr.group(0)
                Repl = self._Get(Find)
                aStr = aStr.replace(Find, Repl)
        return aStr


def FormatFile(aFile: str, aData: dict) -> str:
    with open(aFile, 'r', encoding='utf-8') as F:
        Data = F.read()
    return Data.format(**aData)
