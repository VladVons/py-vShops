# Created: 2024.12.07
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from ._Common import TSpecBase


class TSpecGrade(TSpecBase):
    def _GetPatterns(self) -> dict:
        Res = {
            'grade': [
                # classs A | kl.A | klasa B+
                r'(grade|class|klasa|kl[\.]|клас)\s*(?P<grade>[abc\+\-])',

                # (A) | (B+)
                r'\((?P<grade>[abc\+\-])\)',

                # A<eol> | B+<eol>
                r'\b(?P<grade>[abc\+\-])$'
            ]
        }
        return Res

    def _OnParse(self, aRes: dict, aKey: str, aMatch):
        Groups = aMatch.groupdict()
        aRes[aKey] = Groups.get('grade').lower()
