# Created: 2022.10.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.DbList import TDbList


class TDbProductEx(TDbList):
    def __init__(self):
        super().__init__([
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
        ])

class TDbCategory(TDbList):
    def __init__(self):
        super().__init__([
            'id',
            'parent_id',
            'name'
        ])

class TDbCompPC(TDbList):
    def __init__(self):
        super().__init__([
            'model',
            'case',
            'cpu',
            'disk_size',
            'disk',
            'ram_size',
            'os',
            'vga',
            'dvd',
            'price'
        ])

class TDbCompPricePl(TDbList):
    def __init__(self):
        super().__init__([
            'model'
        ])
