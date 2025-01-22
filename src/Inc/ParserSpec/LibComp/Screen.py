# Created: 2024.12.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from Inc.Var.Str import ToInt
from .._Common import TSpecBase


class TSpecScreenResol(TSpecBase):
    def _GetPatterns(self) -> dict:
        return self._LoadPatternsFile()

    def _OnParse(self, aRes: dict, aKey: str, _aMatch) -> bool:
        aRes['screen_resol'] = aKey
        return True

class TSpecScreenSize(TSpecBase):
    def _GetPatterns(self) -> dict:
        Res = {
            'size': [
                # 12" | 13.5" | 14 zoll| !4x3.5"
                r'(?<!\dx)(?P<size>\d{1,2})(?:[\.,]\d)?\s*-?(?:"|zoll|inch)'
            ]
        }
        return Res

    def _OnParse(self, aRes: dict, aKey: str, aMatch) -> bool:
        Groups = aMatch.groupdict()
        Size = Groups.get('size')
        aRes['screen_size'] = ToInt(Size)
        return True
