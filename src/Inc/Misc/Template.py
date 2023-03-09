# Created: 2023.03.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re


class TDictRepl:
    def __init__(self, aDict: dict = None):
        self.Dict = aDict

        #self.ReVar = re.compile(r'(\$\w+)\b')
        self.ReVar = re.compile(r'(\$[a-zA-Z0-9]+)')

    def Parse(self, aStr: str) -> str:
        if (self.Dict):
            Arr = self.ReVar.search(aStr)
            while (Arr):
                Find = Arr.group(0)
                Repl = self.Dict.get(Find, '-x-')
                aStr = aStr.replace(Find, Repl)
                Arr = self.ReVar.search(aStr)

            self.Dict = {}
        return aStr


def FormatFile(aFile: str, aData: dict) -> str:
    with open(aFile, 'r', encoding='utf-8') as F:
        Data = F.read()
    return Data.format(**aData)
