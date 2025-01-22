# Created: 2024.12.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from ._Common import Lang
from .._Common import TSpecBase


class TSpecRam(TSpecBase):
    def _GetPatterns(self) -> dict:
        Res = {
            'ram': [
                # 8 ram | 16 ram
                r'\b(?P<size>\d{1,2})\s*(?:ram)',

                # 8 ddr3 | 16 lpddr4
                r'\b(?P<size>\d{1,2})\s*(?:lpddr[345]|ddr[345])',

                # ddr3 8| lpddr4 16
                r'(?:lpddr[345]|ddr[345])\s*(?P<size>\d{1,2})',

                # 4Gb 16 gb
                r'\b(?P<size>\d{1,2})\s*(?P<unit>gb|гб)',

                # /16/ | / 4 /
                r'/\s*(?P<size>\d{1,2})\s*/'
            ]
        }
        return Res

    def _OnParse(self, aRes: dict, aKey: str, aMatch):
        Groups = aMatch.groupdict()

        Unit = Groups.get('unit', 'gb')
        aRes['ram'] = {
            'size': int(Groups.get('size')),
            'unit': Lang.Translate(Unit)
        }
