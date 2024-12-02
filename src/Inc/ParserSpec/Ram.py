# Created: 2024.12.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from .Common import TSpecBase


class TSpecRam(TSpecBase):
    def _GetPatterns(self) -> list[str]:
        return [
            # 8 ram | 16 ram
            r'(\d{1,2})\s*(?:ram)',

            # 8 ddr3 | 16 lpddr4
            r'\s(\d{1,2})\s*(?:lpddr[3,4]|ddr[3,4])',

            # ddr3 8| lpddr4 16
            r'(?:lpddr[3,4]|ddr[3,4])\s*(\d{1,2})',

            # 4Gb 16 gb
            r'(\d{1,2})\s*(gb)'
        ]
