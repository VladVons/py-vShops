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
        self.ReVar = re.compile(r'(\$[a-zA-Z0-9_]+)\b')

    def _Get(self, aFind: str) -> str:
        Res = self.Dict.get(aFind)
        if (not Res):
            Strip = re.sub(r'[^\w]', '', aFind)
            Res = f'-{Strip}-'
        return Res

    def Parse(self, aStr: str) -> str:
        if (aStr and self.Dict) :
            while (True):
                Arr = self.ReVar.search(aStr)
                if (not Arr):
                    break

                Find = Arr.group(0)
                Repl = self._Get(Find)
                aStr = aStr.replace(Find, Repl)
        return aStr

    def InPlace(self, aKeys: list[str]):
        for xKey in aKeys:
            Str = self.Dict.get(xKey)
            if (Str):
                R = self.Parse(Str)
                self.Dict[xKey] = R

    def ParseFile(self, aFile: str) -> str:
        with open(aFile, 'r', encoding='utf-8') as F:
            Data = F.read()
        return self.Parse(Data)


def FormatFile(aFile: str, aFormat: dict) -> str:
    with open(aFile, 'r', encoding='utf-8') as F:
        Data = F.read()
    return Data.format(**aFormat)

def FormatFilePkg(aPkg: str, aFile: str, aFormat: dict = None) -> str:
    Dir = aPkg.replace('.', '/')
    return FormatFile(f'{Dir}/{aFile}', aFormat or {})
