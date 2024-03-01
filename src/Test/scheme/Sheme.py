o       #!/usr/bin/env python3

import json
from bs4 import BeautifulSoup
#
from Inc.Scheme.Parser import TSchemeBase
from Inc.Scheme.Scheme import TSoupScheme
from Inc.Scheme.SchemeApi import TSchemeApi
from Inc.Scheme.SchemeApiBase import TSchemeApiBase


class TScheme2(TSchemeBase):
    def ParsePipe(self, aObj, aItem: list, aPath: str) -> object:
        if (hasattr(TSchemeApi, aItem[0])):
            aObj = self._CallPipe(aObj, aItem, aPath, TSchemeApiBase)
        else:
            aObj = self._ParsePipeDef(aObj, aItem, aPath)

        if (aObj is None):
            self.Err.append('%s->%s (none)' % (aPath, aItem))
        return aObj

def DictHoriz(aData: object, aKeys: list, aRes: dict):
    if (isinstance(aData, dict)):
        for Key, Val in aData.items():
            DictHoriz(Val, aKeys, aRes)
            if (Key in aKeys):
                aRes[Key] = Val

def TestJson(aMod: str, aExt: str = '.html'):
    print(aMod, aExt)

    with open(aMod + '.json', 'r', encoding='utf8') as hFile:
        Data = hFile.read()
    Scheme = json.loads(Data)

    with open(aMod + aExt, 'r', encoding='utf8') as hFile:
        Data = hFile.read()

    Soup = BeautifulSoup(Data, 'lxml')
    SoupScheme = TSoupScheme()
    Res = SoupScheme.Parse(Soup, Scheme)
    print(Res)
    print()
    print(SoupScheme.Err)
    Arr = {}
    DictHoriz(Res, ['Image', 'Price', 'Name', 'Stock', 'MPN'], Arr)
    print(Arr)

def Test1():
    Data = '1234 567.8'
    Pipe = [
        ["split", [" ", 1]],
        ["txt2float"]
    ]

    Scheme = TScheme2()
    Res = Scheme.ParsePipes(Data, Pipe, '')
    print('done', Res)

Test1()
#TestJson('bscanner.com.ua')
