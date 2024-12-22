# Created: 2024.12.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Var.Str import ToInt
from ._Common import TSpecBase

class TSpecScreenResol(TSpecBase):
    def _GetPatterns(self) -> dict:
        Res = {
            '4k': [
                r'\b('
                r'b4k|'
                r'3840x2160|'
                r'uhd'
                r')\b'
            ],
            'qhd': [
                r'\b('
                r'2560x1440|'
                r'1440p|'
                r'qhd'
                r')\b'
            ],
            'fhd': [
                r'\b('
                r'1920x1080|'
                r'1080p|'
                r'fhd|'
                r'full hd'
                r')\b'
            ],
            'hd': [
                r'\b('
                r'1366x768|'
                r'720p|'
                r'hd'
                r')\b'
            ]
        }
        return Res

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
