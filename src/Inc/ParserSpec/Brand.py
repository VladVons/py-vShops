# Created: 2024.12.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import re
from ._Common import TSpecBase


class TSpecBrand(TSpecBase):
    reModel = re.compile(r'^[a-z0-9-]+\s*[a-z0-9-]+', re.IGNORECASE)
    Alias = {
        'hewlett': 'hp',
        'hewlett packard': 'hp',
        'hewlett-packard': 'hp',
        'hpe': 'hp',
        'compaq': 'hp'
    }

    def _GetPatterns(self) -> dict:
        return self._LoadPatternsFile()

    def _OnParse(self, aRes: dict, aKey: str, aMatch):
        if (aKey == 'brands'):
            Brand = aMatch.group(0).lower()
            aRes['brand'] = self.Alias.get(Brand, Brand)

            Rest =  aMatch.string[aMatch.regs[0][1]:].strip()
            Match = self.reModel.search(Rest)
            if (Match):
                aRes['model'] = Match.group(0).lower()
        else:
            aRes['brand'] = aKey
        return True

    def GetFields(self) -> list:
        return ['brand', 'model']
