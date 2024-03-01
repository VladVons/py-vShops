# Created: 2022.10.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.DbList import TDbList
from Inc.Scheme.Parser import TSchemeBase
from Inc.Scheme.SchemeApiBase import TSchemeApiBase
from Inc.Util.Obj import GetNotNone


def GetTitle(aRow: dict, aKeys: list, aDelim) -> str:
    Res = []
    for Key in aKeys:
        if (isinstance(Key, list)):
            Val = GetTitle(aRow, Key, ' ')
        else:
            Val = str(aRow.get(Key, ''))
        Res.append(Val)
    return aDelim.join(Res)

def GetTitleValues(aData: dict, aFields: list[str]) -> list:
    Res = []
    for x in aFields:
        Val = str(GetNotNone(aData, x, ''))
        if (Val):
            Res.append(Val)
    return Res

def GetAttr(aRow: dict, aMeta: dict) -> dict:
    Res = {}
    for Key, Val in aMeta.items():
        Data = aRow[Val['field']]
        if (Data):
            if ('delim' in Val):
                Idx = Val['idx']
                Arr = Data.split(Val['delim'])
                if (len(Arr) > Idx):
                    Res[Key] = Arr[Idx]
            else:
                Res[Key] = Data
    return Res


class TDbProductEx(TDbList):
    def __init__(self):
        super().__init__(
            aFields = [
                'id',
                'category_id',
                'code',
                'price',
                'price_in',
                'qty',
                'image',
                'name',
                'summary',
                'features',
                'descr',
                'vendor',
                'cond',
                'attr'
            ]
        )

class TDbCategory(TDbList):
    def __init__(self):
        super().__init__(
            aFields = [
                'id',
                'parent_id',
                'name'
            ]
        )

class TDbCompPC(TDbList):
    def __init__(self):
        super().__init__(
            aFields = [
                'code',
                'case',
                'cpu',
                'disk_size',
                'disk',
                'ram_size',
                'os',
                'vga',
                'dvd',
                'grade',
                'title',
                'price',
                'price_in',
                'qty',
                'cond',
                'attr'
            ],
            aDef = {
                'os': 'NoOS',
                'qty': 0
            }
        )

class TDbCompMonit(TDbList):
    def __init__(self):
        super().__init__(
            aFields = [
                'code',
                'screen',
                'grade',
                'color',
                'title',
                'price',
                'price_in',
                'qty',
                'cond',
                'attr'
            ]
        )

class TDbPrinter(TDbList):
    def __init__(self):
        super().__init__(
            aFields = [
                'code',
                'pages',
                'title',
                'price',
                'price_in',
                'qty',
                'cond',
                'attr'
            ]
        )

class TDbCompPricePl(TDbList):
    def __init__(self):
        super().__init__([
            'model'
        ])

class TDbCrawl(TDbList):
    def __init__(self):
        super().__init__(
            aFields = [
                'tenant',
                'code',
                'url',
                'model',
                'category',
                'product',
                'image',
                'features',
                'descr'
            ]
        )

class TScheme(TSchemeBase):
    def ParsePipe(self, aObj, aItem: list, aPath: str) -> object:
        if (hasattr(TSchemeApiBase, aItem[0])):
            aObj = self._CallPipe(aObj, aItem, aPath, TSchemeApiBase)
        else:
            aObj = self._ParsePipeDef(aObj, aItem, aPath)

        if (aObj is None):
            self.Err.append('%s->%s (none)' % (aPath, aItem))
        return aObj

    def ParsePipes(self, aObj, aScheme: dict, aPath: str = '') -> object:
        Res = {}
        for Key, Val in aScheme.items():
            if (isinstance(Val, list)):
                Obj = aObj
                for x in Val:
                    Obj = self.ParsePipe(Obj, x, f'{aPath}/{Key}')
                    if (Obj is None):
                        break
            else:
                Obj = aObj[Val]

            if (Obj is not None):
                Res[Key] = Obj
        return Res
