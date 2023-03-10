# Created: 2022.10.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.DbList import TDbListSafe, TDbList


class TDbListEx(TDbList):
    def __init__(self, aFields):
        aFields = [Name for Name, _Type in aFields]
        super().__init__(aFields)

class TDbProduct(TDbListEx):
    def __init__(self):
        super().__init__([
            ('id', int),
            ('category_id', int),
            ('code', str),
            ('mpn', str),
            ('name', str),
            ('price', float),
            ('image', str)
        ])

class TDbProductEx(TDbListEx):
    def __init__(self):
        super().__init__([
            ('id', int),
            ('category_id', int),
            ('code', str),
            ('barcode', str),
            ('mpn', str),
            ('name', str),
            ('price', float),
            ('image', list),
            ('feature', dict),
            ('vendor', str),
            ('available', int),
            ('descr', str)
        ])

class TDbPrice(TDbListEx):
    def __init__(self):
        super().__init__([
            ('id', int),
            ('category_id', int),
            ('code', str),
            ('mpn', str),
            ('name', str),
            ('price', float),
            ('available', int),
            ('image', str)
        ])

class TDbCategory(TDbListEx):
    def __init__(self):
        super().__init__([
            ('id', int),
            ('parent_id', int),
            ('name', str)
        ])

class TDbPriceJoin(TDbListEx):
    def __init__(self):
        super().__init__([
            ('id', int),
            ('code', str),
            ('mpn', str),
            ('name', str),
            ('match', int),
            ('price', float)
        ])

class TDbCompPC(TDbListEx):
    def __init__(self):
        super().__init__([
            ('model', str),
            ('case', str),
            ('cpu', str),
            ('disk_size', int),
            ('disk', str),
            ('ram_size', int),
            ('os', str),
            ('vga', str),
            ('dvd', str),
            ('price', float)
        ])

class TDbCompPricePl(TDbListEx):
    def __init__(self):
        super().__init__([
            ('model', str)
        ])
