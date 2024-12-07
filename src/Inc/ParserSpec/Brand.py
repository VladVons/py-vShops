# Created: 2024.12.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import re
from ._Common import TSpecBase


class TSpecBrand(TSpecBase):
    reModel = re.compile(r'^[a-z0-9-]+\s*[a-z0-9-]+', re.IGNORECASE)

    def _GetPatterns(self) -> dict:
        Res = {
            'brand': [
                r'\b('
                r'asus|acer|aoc|apple|'
                r'benq|brother|'
                r'canon|cisco|'
                r'dell|'
                r'eizo|epson|'
                r'ibm|iiyama|'
                r'fujitsu-siemens|fujitsu|'
                r'hp|hewlett[- ]packard|huawei|'
                r'kyocera|konica|'
                r'lenovo|lexmark|lg|'
                r'msi|medion|microsoft|motorola|'
                r'nec|'
                r'oki|'
                r'philips|panasonic|'
                r'samsung|sharp|sony|'
                r'toshiba|'
                r'viewsonic|'
                r'wortmann|'
                r'zebra|'
                r'xerox|xiaomi'
                r')\b'
            ]
        }
        return Res

    def _OnParse(self, aRes: dict, aKey: str, aMatch):
        aRes[aKey] = aMatch.group(0).lower()

        Rest =  aMatch.string[aMatch.regs[0][1]:].strip()
        Match = self.reModel.search(Rest)
        if (Match):
            aRes['model'] = Match.group(0).lower()
