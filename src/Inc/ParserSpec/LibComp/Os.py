# Created: 2024.12.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from .._Common import TSpecBase


class TSpecOs(TSpecBase):
    def _GetPatterns(self) -> dict:
        Res = {
            'os_win': [
                # windows 7, w11p, win 11 pro
                r'(?P<os>windows|win|w)\s*(?P<ver>7|8|10|11|2012|2016|2019)\s*(pro|p|home|h)?'
            ]
        }
        return Res

    def _OnParse(self, aRes: dict, aKey: str, aMatch):
        if (aKey == 'os_win'):
            aRes['os'] = f'windows {aMatch.group(2)}'
        else:
            super()._OnParse(aRes, aKey, aMatch)
