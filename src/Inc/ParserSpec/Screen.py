# Created: 2024.12.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from .Common import TSpecBase

class TResolution(TSpecBase):
    def _GetPatterns(self) -> dict:
        Res = {
            '4k': [
                r'(4k)',
                r'(3840x2160)',
                r'(uhd)'
            ],
            'qhd': [
                r'(2560x1440)',
                r'(1440p)',
                r'(qhd)'
            ],
            'fhd': [
                r'(1920x1080)',
                r'(1080p)',
                r'(fhd)'
            ],
            'hd': [
                r'(1366x768)',
                r'(720p)',
                r'(hd)'
            ]
        }
        return Res

class TSize(TSpecBase):
    def _GetPatterns(self) -> dict:
        Res = {
            'size': [
                # 12.5"
                r'(\d{1,2}(\.\d{1})?)"'
            ]
        }
        return Res

class TSpecScreen(TSpecBase):
    def _GetPatterns(self) -> dict:
        Res = {
            '-size': TSize(),
            'screen': TResolution()
        }
        return Res
