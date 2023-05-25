# Created: 2022.10.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.DbList import TDbList


class TDbProductEx(TDbList):
    def __init__(self):
        super().__init__(
            aFields = [
                'id',
                'category_id',
                'code',
                'barcode',
                'mpn',
                'name',
                'price',
                'image',
                'feature',
                'vendor',
                'available',
                'descr'
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
                'model',
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
                'model',
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
            'mpn',
            'ean',
            'url',
            'category',
            'product',
            'image',
            'features',
            'descr'
        ])
