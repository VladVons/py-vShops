# Created: 2024.12.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from .Common import TSpecBase

class TResolution(TSpecBase):
    def _GetPatterns(self) -> dict:
        Res = {
            '4k': [
                r'4k',
                r'3840x2160',
                r'\buhd\b'
            ],
            'qhd': [
                r'2560x1440',
                r'1440p',
                r'\bqhd\b'
            ],
            'fhd': [
                r'1920x1080',
                r'1080p',
                r'\bfhd\b'
            ],
            'hd': [
                r'1366x768',
                r'720p',
                r'\bhd\b'
            ]
        }
        return Res

    def _OnParse(self, aRes: dict, aKey: str, _aMatch):
        aRes['resolution'] = aKey

class TSize(TSpecBase):
    def _GetPatterns(self) -> dict:
        Res = {
            'size': [
                # 12" | 13.5" | 14 zoll
                r'(\d{1,2})([\.,]\d)?\s*(?:"|zoll|inch)'
            ]
        }
        return Res

class TSpecScreen(TSpecBase):
    def _GetPatterns(self) -> dict:
        Res = {
            'size': TSize(),
            'screen': TResolution()
        }
        return Res
