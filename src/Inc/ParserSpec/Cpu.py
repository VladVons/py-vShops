# Created: 2024.12.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
#
from ._Common import TSpecBase


class TSpecCpu(TSpecBase):
    reGenDigits = re.compile(r'(\d{4,5})')

    def _GetPatterns(self) -> dict:
        Res = {
            'intel': [
                # i3 7G | i5-7G | i7 12Gen | i9-7Gen
                r'(?P<family>i[3579])\s*-?(?P<gen>\d{1,2})\s*(?:g|gen)',

                # i3 G7 | i5-G7 | i7 Gen12 | i9-Gen7
                r'(?P<family>i[3579])\s*-?(?:g|gen)(?P<gen>\d{1,2})',

                # Core2Duo E7200 | Core2 Quad Q8200 | INTELCORE2 DUO-E8400
                r'(?P<family>core\s*2)\s*(?:duo|quad)\s*-?(?P<gen>[a-z]\d{3,4})',

                # Ultra 5 125 | Ultra 7 165H
                r'(?P<family>ultra\s*[3579])\s*(?P<gen>\d{3}[a-z]?)',

                # Pentium 2117U | Pentium-2117 | Pentium T4500 | celeron G1820
                r'(?P<family>pentium|celeron)\s*-?(?P<gen>[a-z]?\d{3,4}[a-z]?)',

                # i5 (i5-3320M) | i3 6300 | i5-6300U
                r'(?P<family>i[3579])\s*-?(?P<gen>\d{3,5}[a-z]{0,2})',

                # i3 | i5
                r'(?P<family>i[3579])'
            ],
            'amd': [
                # A9-9410 | R7 F9410 | R5-9410F | !R5-9410gb
                r'(?P<family>[ra][3579])\s*-?(?P<gen>\d{3,5}(?!gb)[a-z]{0,2})',

                r'(?P<family>sempron) (M100)',
                r'(?P<family>ryzen ai 9)',
                r'(?P<family>ryzen)\s*([3579])\s*(?:pro)?\s*(?P<gen>\d{3,5}[a-z]{0,2})',
                r'(?P<family>ryzen)\s*([3579])'
            ]
        }
        return Res

    def _OnParse(self, aRes: dict, aKey: str, aMatch):
        Groups = aMatch.groupdict()
        if (aKey == 'intel') and ('gen' in Groups):
            Gen = Groups['gen']
            if (len(Gen) > 2):
                Match = self.reGenDigits.search(Gen)
                if (Match):
                    Gen = Match.group(1)
                    GenAlias = Gen[:2] if (Gen.startswith('1')) else Gen[0]
                    Groups['gen_short'] = GenAlias
            else:
                Groups['gen_short'] = Gen
        aRes['cpu'] = Groups
        return True
