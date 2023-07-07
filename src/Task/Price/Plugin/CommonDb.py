# Created: 2022.10.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.DbList import TDbList


def GetTitle(aRow: dict, aKeys: list, aDelim) -> str:
    Res = []
    for Key in aKeys:
        if (isinstance(Key, list)):
            Val = GetTitle(aRow, Key, ' ')
        else:
            Val = str(aRow.get(Key, ''))
        Res.append(Val)
    return aDelim.join(Res)


class TDbProductEx(TDbList):
    def __init__(self):
        super().__init__(
            aFields = [
                'id',
                'category_id',
                'code',
                'price',
                'qty',
                'image',
                'name',
                'summary',
                'features',
                'descr',
                'vendor'
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
                'price',
                'grade',
                'title'
            ],
            aDef = {
                'os': 'NoOS'
            }
        )

class TDbCompMonit(TDbList):
    def __init__(self):
        super().__init__(
            aFields = [
                'code',
                'screen',
                'price',
                'grade',
                'color',
                'title'
            ]
        )

class TDbCompPricePl(TDbList):
    def __init__(self):
        super().__init__([
            'model'
        ])

class TDbCrawl(TDbList):
    def __init__(self):
        super().__init__([
            'tenant',
            'code',
            'url',
            'model',
            'category',
            'product',
            'image',
            'features',
            'descr'
        ])
