# Created: 2024.12.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import re
from ._Common import TSpecBase


class TSpecBrand(TSpecBase):
    reModel = re.compile(r'^[a-z0-9-]+\s*[a-z0-9-]+', re.IGNORECASE)

    def _GetPatterns(self) -> dict:
        Res = {
            'brands': [
                r'\b('
                r'asus|acer|aoc|apple|asotel|aruba|'
                r'benq|brother|'
                r'canon|cisco|clevo|'
                r'dell|d[-\s]?link|dynabook|dicota|'
                r'eizo|epson|'
                r'fujitsu-siemens|fujitsu|'
                r'google|gvc|gateway|getac|gigabyte|'
                r'hp|hewlett[-\s]packard|hpe|huawei|honeywell|hannspree|'
                r'ibm|iiyama|'
                r'juniper|jabra|'
                r'kyocera|konica|koorui|'
                r'lenovo|lexmark|lg|lancom|'
                r'msi|medion|microsoft|motorola|mikrotik|'
                r'nec|nvidia|netapp|netgear|nokia|'
                r'oki|'
                r'philips|panasonic|plantronics|poly|'
                r'qlogic|'
                r'ricoh|'
                r'samsung|sharp|sony|sandisk|seagate|'
                r'toshiba|tp[-\s]?link|terra|'
                r'viewsonic|'
                r'wortmann|'
                r'xerox|xiaomi|'
                r'zyxel|zebra'
                r')\b'
            ],
            'apple': [
                r'\b('
                r'iphone|ipad|macbook'
                r')\b'
            ],
            'acer': [
                r'\b('
                r'veriton'
                r')\b'
            ]
        }
        return Res

    def _OnParse(self, aRes: dict, aKey: str, aMatch):
        if (aKey == 'brands'):
            aRes['brand'] = aMatch.group(0).lower()
            Rest =  aMatch.string[aMatch.regs[0][1]:].strip()
            Match = self.reModel.search(Rest)
            if (Match):
                aRes['model'] = Match.group(0).lower()
        else:
            aRes['brand'] = aKey
        return True
