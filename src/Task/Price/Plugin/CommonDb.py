# Created: 2022.10.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.DbList import TDbList
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
                'used'
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
                'used'
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
                'used'
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
                'used'
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
