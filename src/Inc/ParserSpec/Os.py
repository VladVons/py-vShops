# Created: 2024.12.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from .Common import TSpecBase


class TSpecOs(TSpecBase):
    def _GetPatterns(self) -> list[str]:
        return [
            # windows 7, w11p, win 11 pro
            r'(windows|win|w)\s*(7|8|10|11)\s*(pro|p|home|h)?'
        ]
