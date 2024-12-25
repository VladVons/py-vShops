# Created: 2024.12.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import re
from ._Common import TSpecBase, ToGbUnit, Lang

def GetStorageType(aVal: str) -> str:
    if (not aVal):
        aVal = 'hdd'
    else:
        aVal = aVal.lower()
        if (aVal in ['nvme', 'm2', 'm.2']):
            aVal = 'nvme'
    return aVal

class TSpecStorage(TSpecBase):
    reDigits = re.compile(r'(\d{1,2})')

    def _GetPatterns(self) -> dict:
        Res = {
            'storage': [
                # 12x256 ssd | 512 hdd
                r'((?P<qty>\d{1,2})\s*x\s*)?(?P<size>\d{3,4})\s*(?P<type>ssd|hdd|nvme|m2|m\.2|sas)',

                # ssd 12x256  | hdd 512
                r'(?P<type>ssd|hdd|nvme|m2|m\.2|sas)\s*((?P<qty>\d{1,2})\s*x\s*)?(?P<size>\d{3,4})',

                # 3x 512Gb | 2048 gb | 256gb-ssd
                r'((?P<qty>\d{1,2})\s*x\s*)?(?P<size>\d{3,4})\s*(?P<unit>gb|гб)\s*-?(?P<type>ssd|hdd|nvme|m2|m\.2|sas)?',

                # 3x2tb | 2tb | 12 tb
                r'((?P<qty>\d{1,2})\s*x\s*)?(?P<size>\d{1,2})\s*(?P<unit>tb|тб)\s*-?(?P<type>ssd|hdd|nvme|m2|m\.2|sas)?',

                # /256/ | / 1024 /
                r'/\s*(?P<size>\d{3,4})\s*/'
            ]
        }
        return Res

    def _OnParse(self, aRes: dict, aKey: str, aMatch):
        Groups = aMatch.groupdict()

        Unit = Groups.get('unit', 'gb')
        Size, Unit = ToGbUnit(int(Groups.get('size')), Lang.Translate(Unit))
        Type = GetStorageType(Groups.get('type'))

        Qty = Groups.get('qty')
        if (Qty):
            Size *= int(Qty)

        aRes['storage'] = {
            'size': Size,
            'unit': Unit,
            'type': Type
        }
