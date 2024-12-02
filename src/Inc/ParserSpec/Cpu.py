# Created: 2024.12.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from .Common import TSpecBase


class TSpecCpu(TSpecBase):
    def _GetPatterns(self) -> dict:
        Res = {
            'cpu': [
                # i3 7G | i5-7G | i7 12Gen | i9-7Gen
                r'(i[3579])\s*-?(\d{1,2})\s*(?:g|gen)',

                # i3 G7 | i5-G7 | i7 Gen12 | i9-Gen7
                r'(i[3579])\s*-?(?:g|gen)(\d{1,2})',

                # Core2Duo E7200 | Core2 Quad Q8200 | INTELCORE2 DUO-E8400
                r'(core2)\s*(duo|quad)\s*-?([a-z]\d{3})',

                # Ultra 5 125 | Ultra 7 165H
                r'(ultra [3579]) (\d{3}[a-z]?)',

                # Pentium 2117U | Pentium-2117
                r'(pentium)\s*-?(\d{3,4}[a-z]?)',

                # i5 (i5-3320M) | i3 6300 | i5-6300U
                r'(i[3579])\s*-?(\d{3,4}[a-z]?)',

                # i3 | i5
                r'(i[3579])'
            ]
        }
        return Res